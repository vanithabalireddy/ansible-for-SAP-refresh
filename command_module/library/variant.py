from sap_system_refresh.src.PreSystemRefresh import *
from templates.export_printer_devices_vars import *
import sys


def main(args):

    options = ["create", "delete", "check"]
    if len(args) > 2:
        raise Exception("Python script takes exactly one argument [create|delete|check]")
    if str(args[1]) not in options:
        raise Exception("Python script accepts only either [create|delete|check] args")

    sysRefresh = PreSystemRefresh()

    if str(args[1]) == "create":
        print(sysRefresh.create_variant(report, variant_name, desc, content, text, screen))
    elif str(args[1]) == "delete":
        print(sysRefresh.delete_variant(report, variant_name))
    elif str(args[1]) == "check":
        print(sysRefresh.check_variant(report, variant_name))
    else:
        return "Please check the option specified [create|delete|check]"

if __name__ == '__main__':
    main(sys.argv)


