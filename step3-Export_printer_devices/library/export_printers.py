#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh
from ansible.module_utils.export_printer_devices_vars import *


def main():

    fields = {
        "report": {"required": True, "type": "str"},
        "variant_name": {"required": True, "type": "str"},
    }

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes" : "CheckMode is not supported as of now!"})

    report = module.params['report']
    variant_name = module.params['variant_name']

    sysRefresh = PreSystemRefresh()

    if report and variant_name:
        result = sysRefresh.export_printer_devices(report, variant_name)

    module.exit_json(changed=True, stdout="{}".format(result))

if __name__ == "__main__":
    main()

