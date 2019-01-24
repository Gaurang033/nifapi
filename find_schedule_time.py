__author__ = "Gaurang Shah"
__version__ = "1.0.0"
__maintainer__ = "Gaurang Shah"
__email__ = "gaurang.shah@cantire.com"

import requests
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import utils


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

OUTPUT_FILE = open("%s.out" % os.path.basename(__file__), "w+")


def _find_processor_schedule(group_id, group_name):
    url = "https://%s:%s/nifi-api/process-groups/%s/processors" % (utils.NIFI_HOST, utils.NIFI_PORT, group_id)
    header = {"Authorization": "Bearer %s" % utils.ACCESS_TOKEN}
    r = requests.get(url, headers=header, verify=False)
    resp = r.json()

    processors = resp.get("processors")

    for processor in processors:
        component = processor.get("component")
        config = component.get("config")
        if component.get("state") == "RUNNING" and config.get("schedulingStrategy") == "CRON_DRIVEN":
            print >>OUTPUT_FILE, "%s,%s,%s,%s" % (group_id, group_name, processor.get("id"), config.get("schedulingPeriod"))


def find_schedule(processor_groups):
    for processor_group in processor_groups:
        p = processor_group.get("processGroupStatusSnapshot")
        if len(p.get("processGroupStatusSnapshots")) > 0:
            find_schedule(p.get("processGroupStatusSnapshots"))
        else:
            _find_processor_schedule(p.get("id"), p.get("name"))


if __name__ == '__main__':
    username, password = utils.read_credential_from_console()
    token = utils.get_token(username, password)
    utils.ACCESS_TOKEN = token
    root_processor = utils.get_root_processor()
    find_schedule(root_processor)
