"""Module for using provide api"""
import logging
import requests


class Provider:  # pylint: disable=too-few-public-methods
    """Reuseable code between different providers.
    ---

    This class implements methods that can be used from different providers.
    """

    def __init__(self, CONFIG, version):
        self.Config = CONFIG
        self.log = logging.getLogger("PDDNS")
        self.version = version

    def update_nic(self, url: str, ip: str):
        """Update ip address with a get request to nic/update:

        https://<login-data>@<url>/nic/update?hostname=<Name>&myip=<ip>

        Args:
            url (str): url of the provider
            ip (str): ip address
        """
        login_data = f"{self.Config['User']}:{self.Config['Password']}"
        BASE_URL = f"https://{login_data}@{url}/nic/update"
        header = {"User-Agent": f"PDDNS v{self.version}"}
        data = {"hostname": self.Config["Name"], "myip": ip}
        r = requests.get(BASE_URL, params=data, headers=header)
        self.log.debug(r.text)
        r.raise_for_status()
