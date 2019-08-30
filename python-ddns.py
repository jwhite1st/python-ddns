# pylint: disable=invalid-name, missing-docstring
import configparser
import socket
import requests
# import ipaddress

base_url = "https://api.cloudflare.com/client/v4/zones/"
config = configparser.ConfigParser()
config.read("config.conf")

# Shamlessly taken from stackoverflow https://stackoverflow.com/a/28950776/11542276
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('1.1.1.1', 1))
        host = s.getsockname()[0]
    except:
        host = '127.0.0.1'
    finally:
        s.close()
    return host


def add_record(ip):
    record = {}
    record["type"] = "A"
    record["name"] = config['Cloudflare']['name']
    record['content'] = ip
    record['proxied'] = config['Cloudflare']['proxied'] == 'True'
    output = post(record)
    print(output)
    if not output['success']:
        try:
            error_code = output['errors'][0]['error_chain'][0]['code']
        except KeyError:
            error_code = output['errors'][0]['code']
        # This error code means the record can not be proxied. Likely due to a private IP
        if error_code == 9041: 
            record['proxied'] = False
            r = post(record)
            if r.json()['success']:
                print("The record was created successfully")
        else:
            print("There was an error\n")
            print(output['errors'])
    if output['success']:
        print("The record was created successfully")


def post(content):
    headers = {'Authorization': config['Cloudflare']['API_Token'],
               "X-Auth-Email": config['Cloudflare']['Email'],
               "Content-Type": "application/json"}
    zone = config['Cloudflare']['Zone']
    api_url = base_url+zone+"/dns_records"
    return requests.post(api_url, json=content, headers=headers).json()
    

add_record(get_ip())
