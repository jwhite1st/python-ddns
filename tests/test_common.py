""" shared modules for tests
"""
import pytest
import pddns.providers.common as common


class MockResponse:  # pylint: disable=too-few-public-methods
    """This class simulate the response of the update request"""

    def __init__(self):
        self.text = "test"

    @staticmethod
    def raise_for_status():
        """Never raise an exception"""
        return "test"


@pytest.mark.parametrize(
    "ip, result",
    [
        ("1.2.3.5", "1.2.3.5"),
        ("fe80::ef15:6e00:90c3:b2a5", "fe80::ef15:6e00:90c3:b2a5"),
        (
            "1.2.3.5,fe80::ef15:6e00:90c3:b2a5",
            "1.2.3.5,fe80::ef15:6e00:90c3:b2a5",
        ),
    ],
)
def test_common(mocker, ip, result):
    """Test for dyndns update for common

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ipv4 {str}: IPv4 address
        ipv6 {str}: IPv6 address
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
