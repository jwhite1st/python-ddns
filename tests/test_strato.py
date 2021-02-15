"""This module test the requests for a dyndns update for strato
"""
import pytest
import tests.test_common as common
import pddns.providers.strato as strato


@pytest.mark.parametrize(
    "ipv4, ipv6, result",
    [
        ("1.2.3.5", "", "1.2.3.5"),
        ("", "fe80::ef15:6e00:90c3:b2a5", "fe80::ef15:6e00:90c3:b2a5"),
        (
            "1.2.3.5",
            "fe80::ef15:6e00:90c3:b2a5",
            "1.2.3.5,fe80::ef15:6e00:90c3:b2a5",
        ),
        ("", "", ValueError),
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
    mock.return_value = common.MockResponse()
    config = {
        "Strato": {
            "Name": "test.strato.de",
            "User": "testuser",
            "Password": "password",
        }
    }
    provider_strato = strato.Strato(config, "1.2.3.4")
    if isinstance(result, type) and issubclass(result, Exception):
        with pytest.raises(ValueError):
            provider_strato.main(ipv4, ipv6)
    else:
        provider_strato.main(ipv4, ipv6)
        mock.assert_called_with(
            "https://testuser:password@dyndns.strato.com/nic/update",
            params={"hostname": "test.strato.de", "myip": result},
            headers={"User-Agent": "PDDNS v1.2.3.4"},
        )
