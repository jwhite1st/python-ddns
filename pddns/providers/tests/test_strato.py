"""This module test the requests for a dyndns update for strato
"""
import pytest
import pddns.providers.strato as strato


class MockResponse:  # pylint: disable=too-few-public-methods
    """This class simulate the response of the update request"""

    def __init__(self):
        self.text = "test"

    @staticmethod
    def raise_for_status():
        """Never raise an exception"""
        return "test"


@pytest.mark.parametrize(
    "ipv4, ipv6, result",
    [
        ("1.2.3.4", "", "1.2.3.4"),
        ("", "fe80::ef15:6e00:90c3:b2a5", "fe80::ef15:6e00:90c3:b2a5"),
        (
            "1.2.3.4",
            "fe80::ef15:6e00:90c3:b2a5",
            "1.2.3.4,fe80::ef15:6e00:90c3:b2a5",
        ),
    ],
)
def test_strato(mocker, ipv4, ipv6, result):
    """Test for dyndns update for strato

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ipv4 {str}: IPv4 address
        ipv6 {str}: IPv6 address
    """

    mock = mocker.patch("requests.get")
    mock.return_value = MockResponse()
    config = {
        "Strato": {
            "Name": "test.strato.de",
            "User": "testuser",
            "Password": "password",
        }
    }
    provider = strato.Strato(config, "V1.2.3.4")
    provider.main(ipv4, ipv6)
    mock.assert_called_with(
        "https://testuser:password@dyndns.strato.com/nic/update",
        params={"hostname": "test.strato.de", "myip": result},
        headers={"User-Agent": "PDDNS vV1.2.3.4"},
    )
