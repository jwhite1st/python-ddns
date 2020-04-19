"""Module for using Cloudflare's API"""
import logging
from typing import Union, Any
import requests


class Cloudflare():
    """Cloudflare
    ---

    Class that deals with records for Cloudflare.
    """
    def __init__(self, CONFIG):
        self.Config = CONFIG
        self.log = logging.getLogger("PDDNS")

        self.log.info("Cloudflare selected")
        self.log.debug(self.Config.items("Cloudflare"))

    def main(self, ip: str) -> None:
        """main
        ---

        Arguments:
        ---
            ip {str} -- The IP address that the new record will have.
        """
        check = self.check_record()
        if check:
            self.update_record(ip, check)
        else:
            self.add_record(ip)

    def check_record(self) -> Union[str, bool]:
        """check_record
        ---

        Checks if an existing record already exists

        Returns:
            Union[str, bool] -- Returns either the record if it
                                exists or False if it does not exist.
        """
        record = {}
        record["type"] = "A"
        record["name"] = self.Config['Cloudflare']['name']
        output = self.send(record, "get")
        if not output["success"]:
            raise Exception("The check failed with error code {}".format(
                output['errors'][0]['code']))
        if output:
            return output
        return False

    def add_record(self, ip: str) -> None:
        """add_record
        ---

        Creates a new A record.

        Arguments:
            ip {str} -- [description]
        """
        record = {}
        record["type"] = "A"
        record["name"] = self.Config['Cloudflare']['name']
        record['content'] = ip
        record['proxied'] = self.Config.getboolean("Cloudflare", "proxied")
        output = self.send(record, "post")
        if not output['success']:
            try:
                error_code = output['errors'][0]['error_chain'][0]['code']
            except KeyError:
                error_code = output['errors'][0]['code']
            else:
                self.log.error("There was an error\n")
                self.log.error(output['errors'])
                self.log.error(error_code)
        if output['success']:
            self.log.info("The record was created successfully")

    def update_record(self, ip: str, record_id: str):
        """update_record
        ---

        Updates an existing record.

        Arguments:
            ip {str} -- The IP Address to be updated.
            record_id {str} -- The record_id of the record to update.
        """
        record = {}
        record["type"] = "A"
        record["name"] = self.Config['Cloudflare']['name']
        record['content'] = ip
        output = self.send(record, "put", record_id)
        if not output['success']:
            self.log.error("There was an error:")
            self.log.error(output)
        else:
            self.log.info("Record updated successfully")

    def send(self, content: dict,
             which: str, extra: str = None) -> Union[Any, bool]:
        """send
        ---

        Function that sends the information

        Arguments:
            content {dict} -- [description]
            which {int} -- [description]

        Keyword Arguments:
            extra {str} -- [description] (default: {None})

        Returns:
            Union[Any, bool] -- [description]
        """
        BASE_URL = "https://api.cloudflare.com/client/v4/zones/"
        api_token = self.Config['Cloudflare']['API_Token']
        headers = {
            "Authorization": "Bearer {}".format(api_token),
            "X-Auth-Email": self.Config['Cloudflare']['Email'],
            "Content-Type": "application/json"}
        zone = self.Config['Cloudflare']['Zone']
        api_url = BASE_URL + zone + "/dns_records"
        # GET Request
        if which == "get":  # pylint: disable=no-else-return
            r = requests.get(api_url, params=content, headers=headers).json()
            self.log.debug(r)
            if r['result']:
                return r['result'][0]['id']
            return r
        # POST Request
        elif which == "post":
            r = requests.post(api_url, json=content, headers=headers).json()
            self.log.debug(r)
            return r
        # PUT Request
        elif which == "put":
            api_url = api_url + "/" + extra
            r = requests.put(api_url, json=content, headers=headers).json()
            self.log.debug(r)
            return r
        return False
