"""Module for using Cloudflare's API"""
import logging
import requests


class Cloudflare():
    """Cloudflare
    ---

    Class that deals with records for Cloudflare.

    Returns:
        [type] -- [description]
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
            ip {[type]} -- [description]
        """
        check = self.check_record()
        self.log.debug("Check: %s", check)
        if check:
            self.update_record(ip, check)
        else:
            self.add_record(ip)

    def check_record(self):
        """Checks if an existing record already exists"""
        record = {}
        record["type"] = "A"
        record["name"] = self.Config['Cloudflare']['name']
        output = self.send(record, 1)
        if output:
            return output
        return False

    def add_record(self, ip) -> None:
        """Creates a new record"""
        record = {}
        record["type"] = "A"
        record["name"] = self.Config['Cloudflare']['name']
        record['content'] = ip
        record['proxied'] = self.Config['Cloudflare']['proxied'] == 'True'
        output = self.send(record, 2)
        if not output['success']:
            try:
                error_code = output['errors'][0]['error_chain'][0]['code']
            except KeyError:
                error_code = output['errors'][0]['code']
            # This error code means the record can not be proxied.
            # Likely due to a private IP
            if error_code == 9041:
                record['proxied'] = False
                r = self.send(record, 2)
                if r.json()['success']:
                    self.log.info("The record was created successfully")
            else:
                self.log.error("There was an error\n")
                self.log.error(output['errors'])
        if output['success']:
            self.log.info("The record was created successfully")

    def update_record(self, ip, record_id):
        """updates an existing record"""
        record = {}
        record["type"] = "A"
        record["name"] = self.Config['Cloudflare']['name']
        record['content'] = ip
        output = self.send(record, 3, record_id)
        if not output['success']:
            self.log.error("There was an error:")
            self.log.error(output)
        else:
            self.log.info("Record updated successfully")

    def send(self, content, which, extra=None):
        """Function that sends the information"""
        BASE_URL = "https://api.cloudflare.com/client/v4/zones/"
        api_token = self.Config['Cloudflare']['API_Token']
        headers = {
            "Authorization": "Bearer {}".format(api_token),
            "X-Auth-Email": self.Config['Cloudflare']['Email'],
            "Content-Type": "application/json"}
        zone = self.Config['Cloudflare']['Zone']
        api_url = BASE_URL + zone + "/dns_records"
        if which == 1:
            r = requests.get(api_url, params=content, headers=headers).json()
            self.log.debug(r)
            if r['result']:
                return r['result'][0]['id']
        elif which == 2:
            r = requests.post(api_url, json=content, headers=headers).json()
            self.log.debug(r)
            return r
        elif which == 3:
            api_url = api_url + "/" + extra
            r = requests.put(api_url, json=content, headers=headers).json()
            self.log.debug(r)
            return r
        return False
