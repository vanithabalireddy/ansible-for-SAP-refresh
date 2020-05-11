#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh
from ansible.module_utils.export_printer_devices_vars import *


def main():

    fields = {
        "report": {"required": True, "type": "str"},
        "variant_name": {"required": True, "type": "str"},
        "action": {"required": True, "type": "str"}
    }

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes" : "CheckMode is not supported as of now!"})

    report = module.params['report']
    variant_name = module.params['variant_name']
    action = module.params['action']

    prefresh = PreSystemRefresh()

    if action == "create":
        result = prefresh.create_variant(report, variant_name, desc, content, text, screen)
    elif action == "delete":
        result = prefresh.delete_variant(report, variant_name)
    elif action == "check":
        result = prefresh.check_variant(report, variant_name)
    else:
        raise AnsibleError("action parameters supports only [create|delete|check]")

    module.exit_json(changed=True, stdout="{}".format(result))


if __name__ == "__main__":
    main()

