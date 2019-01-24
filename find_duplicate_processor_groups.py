__author__ = "Gaurang Shah"
__version__ = "1.0.0"
__maintainer__ = "Gaurang Shah"
__email__ = "gaurang.shah@cantire.com"

import utils
import os

proc_group = {}
OUTPUT_FILE = open("%s.out" % os.path.basename(__file__), "w+")


def find_duplicate_processor_groups(processor_groups):
    for processor_group in processor_groups:
        p = processor_group.get("processGroupStatusSnapshot")
        if len(p.get("processGroupStatusSnapshots")) > 0:
            find_duplicate_processor_groups(p.get("processGroupStatusSnapshots"))
        else:
            # print "%s - %s - %s " % (p.get("id"), p.get("name"), p.get("queuedSize"))
            # stop_processor_group(p.get("id"))
            name = p.get("name")
            global proc_group
            if name in proc_group:
                proc_group[name] = proc_group.get(name)+1
            else:
                proc_group[name] = 1

    return proc_group


if __name__ == '__main__':
    username, password = utils.read_credential_from_console()
    token = utils.get_token(username, password)
    ACCESS_TOKEN = token
    root_processor = utils.get_root_processor()
    groups = find_duplicate_processor_groups(root_processor)

    for k, v in groups.iteritems():
        if v > 1:
            print >>OUTPUT_FILE, "%s,%s" % (k, v)
