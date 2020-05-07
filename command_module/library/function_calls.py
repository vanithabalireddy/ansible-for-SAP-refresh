#!/usr/bin/python
from sap_system_refresh.src.PreSystemRefresh import *
from templates.export_printer_devices_vars import *
import sys


def main():

    if len(sys.argv) > 2:
        raise Exception("Python script takes exactly one argument ['export_printer_devices']")

    sysRefresh = PreSystemRefresh()

    if str(sys.argv[1]) == "export_printer_devices":
        print(sysRefresh.export_printer_devices(report, variant_name))

if __name__ == '__main__':
    main()


