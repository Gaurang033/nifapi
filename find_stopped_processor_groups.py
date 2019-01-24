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


def get_stopped_processor_count(group_id):
    """
    Finds the processor groups with none of the processor running
    :param group_id:
    :return:
    """
    url = "https://%s:%s/nifi-api/process-groups/%s" % (utils.NIFI_HOST, utils.NIFI_PORT, group_id)
    header = {"Authorization": "Bearer %s" % utils.ACCESS_TOKEN}
    r = requests.get(url, headers=header, verify=False)
    resp = r.json()
    running_count = resp.get("runningCount")
    processor_name = resp.get("status").get("name")
    return running_count, processor_name


def find_stopped_processor(group_id):
    running_count, processor_name = get_stopped_processor_count(group_id)
    if int(running_count) == 0:
        print >>OUTPUT_FILE, "%s,%s" % (group_id, processor_name)


def find_processor_group_stopped_processor(processor_groups):
    for processor_group in processor_groups:
        p = processor_group.get("processGroupStatusSnapshot")
        count, name = get_stopped_processor_count(p.get("id"))
        if count == 0:
            print >> OUTPUT_FILE, "%s,%s" % (p.get("id"), name)
        elif len(p.get("processGroupStatusSnapshots")) > 0:
            find_processor_group_stopped_processor(p.get("processGroupStatusSnapshots"))
        else:
            find_stopped_processor(p.get("id"))


if __name__ == '__main__':
    username, password = utils.read_credential_from_console()
    token = utils.get_token(username, password)
    utils.ACCESS_TOKEN = token
    root_processor = utils.get_root_processor()
    find_processor_group_stopped_processor(root_processor)
