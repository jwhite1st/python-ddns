"""This module test the requests for a dyndns update for afraid
"""
import pytest
import tests.test_common as common
import pddns.providers.afraid as afraid


@pytest.mark.parametrize(
    "ipv4, ipv6, result",
    [
        ("1.2.3.4", "", "1.2.3.4"),
        ("", "fe80::ef15:6e00:90c3:b2a5", "fe80::ef15:6e00:90c3:b2a5"),
        (
            "1.2.3.4",
            "fe80::ef15:6e00:90c3:b2a5",
            "fe80::ef15:6e00:90c3:b2a5",
        ),
        ("", "", ValueError),
    ],
)
def test_afraid(mocker, ipv4, ipv6, result):
    """Test for dyndns update for afraid

    Arguments:
    ---
        monkeypatch {Generator}: monkeypatch
        ipv4 {str}: IPv4 address
        ipv6 {str}: IPv6 address
    """

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = common.MockResponse()
    config = {
        "Afraid": {
            "Name": "test.afraid.de",
            "User": "testuser",
            "Password": "password",
        }
    }
    provider_afraid = afraid.Afraid(config, "1.2.3.4")
    if isinstance(result, type) and issubclass(result, Exception):
        with pytest.raises(ValueError):
            provider_afraid.main(ipv4, ipv6)
    else:
        provider_afraid.main(ipv4, ipv6)
        mock_get.assert_called_with(
            "https://testuser:password@freedns.afraid.org/nic/update",
            params={"hostname": "test.afraid.de", "myip": result},
            headers={"User-Agent": "PDDNS v1.2.3.4"},
        )
