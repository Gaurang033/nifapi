__author__ = "Gaurang Shah"
__version__ = "1.0.0"
__maintainer__ = "Gaurang Shah"
__email__ = "gaurang.shah@cantire.com"

import requests
import utils
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


OUTPUT_FILE = open("%s.out" % os.path.basename(__file__), "w+")


def find_invalid_processor(group_id):
    url = "https://%s:%s/nifi-api/process-groups/%s" % (utils.NIFI_HOST, utils.NIFI_PORT, group_id)
    header = {"Authorization": "Bearer %s" % utils.ACCESS_TOKEN}
    r = requests.get(url, headers=header, verify=False)
    resp = r.json()
    invalid_count = resp.get("invalidCount")
    if int(invalid_count) > 0:
        print >>OUTPUT_FILE, "%s,%s,%s" % (group_id, resp.get("status").get("name"), invalid_count)


def find_processor_group_with_invalid_processor(processor_groups):
    for processor_group in processor_groups:
        p = processor_group.get("processGroupStatusSnapshot")
        if len(p.get("processGroupStatusSnapshots")) > 0:
            find_processor_group_with_invalid_processor(p.get("processGroupStatusSnapshots"))
        else:
            find_invalid_processor(p.get("id"))


if __name__ == '__main__':
    username, password = utils.read_credential_from_console()
    utils.ACCESS_TOKEN = utils.get_token(username, password)
    root_processor = utils.get_root_processor()
    find_processor_group_with_invalid_processor(root_processor)
