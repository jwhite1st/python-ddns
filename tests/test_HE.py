"""This module test the requests for a dyndns update for Hurricane Electric
"""
import pytest
import pddns.providers.hurricaneElectric as hurricaneElectric


class MockResponse:  # pylint: disable=too-few-public-methods
    """This class simulate the response of the update request"""

    def __init__(self):
        self.text = "test"

    @staticmethod
    def raise_for_status():
        """Never raise an exception"""
        return "failed"


@pytest.mark.parametrize(
    "ipv4, _, result",
    [
        ("1.2.3.4", "", "1.2.3.4"),
    ],
)
def test_HE(mocker, ipv4, _, result):
    """Test for dyndns update for Hurricane Electric

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ipv4 {str}: IPv4 address
    """

    mock = mocker.patch("requests.post")
    mock.return_value = MockResponse()
    config = {
        "Hurricane Electric": {
            "Name": "test.hurricane.electric",
            "Password": "testpassword",
            "ip": "1.2.3.4",
        }
    }
    provider = hurricaneElectric.HurricaneElectric(config, "1.2.3.4")
    provider.main(ipv4, _)
    mock.assert_called_with(
        "https://dyn.dns.he.net/nic/update",
        data={"hostname": "test.hurricane.electric", "password": "testpassword", "myip": result},
        headers={"User-Agent": "PDDNS v1.2.3.4"},
    )
