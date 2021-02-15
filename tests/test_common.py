""" shared modules for tests
"""
import pytest
import dns.resolver
import pddns.providers.common as common


class MockResponse:  # pylint: disable=too-few-public-methods
    """This class simulate the response of the update request"""

    def __init__(self):
        self.text = "test"

    @staticmethod
    def raise_for_status():
        """Never raise an exception"""
        return "test"


class MockResolver:  # pylint: disable=too-few-public-methods
    """This class simulate the response of the update request"""

    def __init__(self, ipv4, ipv6):
        self.ipv4 = ipv4
        self.ipv6 = ipv6

    def resolve(self, _, rdtype):
        """replace resolve"""
        if rdtype == "A":
            if self.ipv4:
                return [self.ipv4]
            raise dns.resolver.NoAnswer
        if rdtype == "AAAA":
            if self.ipv6:
                return [self.ipv6]
            raise dns.resolver.NoAnswer
        return [None]


@pytest.mark.parametrize(
    "ip, result",
    [
        ("1.2.3.5", "1.2.3.5"),
        (
            "fe80::ef15:6e00:90c3:b2a5",
            "fe80::ef15:6e00:90c3:b2a5",
        ),
        (
            "1.2.3.5,fe80::ef15:6e00:90c3:b2a5",
            "1.2.3.5,fe80::ef15:6e00:90c3:b2a5",
        ),
    ],
)
def test_update_nic(mocker, ip, result):
    """Test for update_nic

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ip {str}: IP address
    """

    mock = mocker.patch("requests.get")
    mock.return_value = MockResponse()
    config = {
        "Name": "test.common.de",
        "User": "testuser",
        "Password": "password",
    }
    provider = common.Provider(config, "1.2.3.4")
    provider.update_nic("dyndns.common.com", ip)
    mock.assert_called_with(
        "https://testuser:password@dyndns.common.com/nic/update",
        params={"hostname": "test.common.de", "myip": result},
        headers={"User-Agent": "PDDNS v1.2.3.4"},
    )


@pytest.mark.parametrize(
    "ipv4, ipv6, dns_resolver, result",
    [
        ("1.2.3.4", "", {"ipv4": "1.2.3.4", "ipv6": None}, True),
        (
            "",
            "fe80::ef15:6e00:90c3:b2a5",
            {"ipv4": None, "ipv6": "fe80::ef15:6e00:90c3:b2a5"},
            True,
        ),
        (
            "1.2.3.4",
            "fe80::ef15:6e00:90c3:b2a5",
            {"ipv4": "1.2.3.4", "ipv6": "fe80::ef15:6e00:90c3:b2a5"},
            True,
        ),
        ("1.2.3.4", "", {"ipv4": "1.2.3.5", "ipv6": None}, False),
        (
            "",
            "fe80::ef15:6e00:90c3:b2a5",
            {"ipv4": None, "ipv6": "fe80::ef15:6e00:90c3:b2a6"},
            False,
        ),
        ("1.2.3.4", "", {"ipv4": None, "ipv6": None}, False),
        (
            "",
            "fe80::ef15:6e00:90c3:b2a5",
            {"ipv4": None, "ipv6": None},
            False,
        ),
    ],
)
def test_is_ip_uptodate(mocker, ipv4, ipv6, dns_resolver, result):
    """Test for dyndns update for common

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ipv4 {str}: IPv4 address
        ipv6 {str}: IPv6 address
    """
    mock_resolve = mocker.patch("dns.resolver.Resolver")
    mock_resolve.return_value = MockResolver(**dns_resolver)
    config = {
        "Name": "test.common.de",
        "User": "testuser",
        "Password": "password",
    }
    provider = common.Provider(config, "1.2.3.4")
    assert provider.is_ip_uptodate(ipv4, ipv6) == result
