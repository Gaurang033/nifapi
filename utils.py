__author__ = "Gaurang Shah"
__version__ = "1.0.0"
__maintainer__ = "Gaurang Shah"
__email__ = "gaurang.shah@cantire.com"

import getpass
import requests

NIFI_HOST = ""
NIFI_PORT = ""
ACCESS_TOKEN = ""


def get_token(username, password):
    url = "https://%s:%s/nifi-api/access/token" % (NIFI_HOST, NIFI_PORT)
    header = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    data = {"username": username, "password": password}

    resp = requests.post(url, data=data, headers=header, verify=False)

    if resp.status_code not in (200, 201):
        print resp.reason
        print resp.text
        exit(1)
    return resp.text


def read_credential_from_console():
    host = raw_input("NiFi Host : ")
    port = raw_input("NiFi Port : ")
    user = raw_input("Username [%s]: " % getpass.getuser())
    password = getpass.getpass()

    global NIFI_HOST
    global NIFI_PORT
    NIFI_HOST = host
    NIFI_PORT = port
    return user, password


def get_root_processor():
    url = "https://%s:%s/nifi-api/flow/process-groups/root/status?recursive=true" % (NIFI_HOST, NIFI_PORT)
    header = {"Authorization": "Bearer %s" % ACCESS_TOKEN}
    resp = requests.get(url, headers=header, verify=False)
    root_processor = resp.json().get("processGroupStatus").get("aggregateSnapshot").get("processGroupStatusSnapshots")
    return root_processor
