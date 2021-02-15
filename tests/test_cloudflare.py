"""Tests for cloudflare provider"""
import pytest
import pddns.providers.cloudflare as cloudflare
from configparser import ConfigParser
import os


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


def make_mock_config():
    CONFIG = ConfigParser(interpolation=None)
    dn = os.path.dirname(os.path.realpath(__file__))
    CONFIG.read(os.path.join(dn, "config.conf"))
    return CONFIG


@pytest.mark.parametrize(
    "ipv4, result",
    [
        ("1.2.3.4", "1.2.3.4"),
    ],
)
def test_cloudflare_get_ip(mocker, ipv4, result):
    """Test for dyndns update for Cloudflare

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ipv4 {str}: IPv4 address
    """
    mock_ip_check = mocker.patch("requests.get")
    mock_ip_check.return_value = MockJSONResponse()
    config = make_mock_config()
    provider = cloudflare.Cloudflare(config, "1.2.3.4")
    provider.check_record()
    mock_ip_check.assert_called_with(
        "https://api.cloudflare.com/client/v4/zones/4/dns_records",
        json={"type": "A", "name": "test.cloudflare.com"},
        headers=default_headers,
    )


@pytest.mark.parametrize(
    "ipv4, result",
    [
        ("1.2.3.4", "1.2.3.4"),
    ],
)
def test_cloudflare_add_record(mocker, ipv4, result):
    mock_record_add = mocker.patch("requests.post")
    mock_record_add.return_value = MockJSONResponse()
    config = make_mock_config()
    provider = cloudflare.Cloudflare(config, "1.2.3.4")
    provider.add_record(ipv4)
    mock_record_add.assert_called_with(
        "https://api.cloudflare.com/client/v4/zones/4/dns_records",
        json={"type": "A", "name": "test.cloudflare.com", "content": ipv4, "proxied": True},
        headers=default_headers
    )


@pytest.mark.parametrize(
    "ipv4, result",
    [
        ("1.2.3.4", "1.2.3.4"),
    ],
)
def test_cloudflare_update_record(mocker, ipv4, result):
    mock_record_update = mocker.patch("requests.put")
    mock_record_update.return_value = MockJSONResponse()
    config = make_mock_config()
    provider = cloudflare.Cloudflare(config, "1.2.3.4")
    provider.update_record(ipv4, "10")
    mock_record_update.assert_called_with(
        "https://api.cloudflare.com/client/v4/zones/4/dns_records/10",
        json={"type": "A", "name": "test.cloudflare.com", "content": ipv4},
        headers=default_headers
    )