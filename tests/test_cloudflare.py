"""Tests for cloudflare provider"""
import pytest
import pddns.providers.cloudflare as cloudflare


class MockJSONResponse:  # pylint: disable=too-few-public-methods
    """This class simulate the response of the update request"""

    def __init__(self):
        self.text = "test"

    @staticmethod
    def raise_for_status():
        """Never raise an exception"""
        return "failed"

    def json(self):
        return {"success": True, "result": False}


default_headers = {
    "Authorization": f"Bearer testpassword",
    "X-Auth-Email": "test@jwhite.network",
    "Content-Type": "application/json",
    "User-Agent": "PDDNS v1.2.3.4",
}


@pytest.mark.parametrize(
    "ipv4, _, result",
    [
        ("1.2.3.4", "", "1.2.3.4"),
    ],
)
def test_cloudflare(mocker, ipv4, _, result):
    """Test for dyndns update for Cloudflare

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ipv4 {str}: IPv4 address
    """
    mock_ip_check = mocker.patch("requests.get")
    mock_ip_check.return_value = MockJSONResponse()
    config = {
        "Cloudflare": {
            "Name": "test.cloudflare.com",
            "API_Token": "testpassword",
            "ip": "1.2.3.4",
            "Zone": "4",
            "Proxied": True,
            "Email": "test@jwhite.network"
        }
    }
    provider = cloudflare.Cloudflare(config, "1.2.3.4")
    provider.check_record()
    mock_ip_check.assert_called_with(
        "https://api.cloudflare.com/client/v4/zones/4/dns_records",
        json={"type": "A", "name": "test.cloudflare.com"},
        headers=default_headers,
    )
