#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh
from ansible.module_utils.variant_data import *


def main():

    fields = dict(
        report=dict(required=True, type='str'),
        variant_name=dict(required=True, type='str'),
        action=dict(required=True, type='str')
    )

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
        prefresh.create_variant(module, report, variant_name, desc, content, text, screen)
    elif action == "delete":
        prefresh.delete_variant(module, report, variant_name)
    elif action == "check":
        prefresh.check_variant(module, report, variant_name)
    else:
        raise AnsibleError("action parameters supports only [create|delete|check]")


if __name__ == "__main__":
    main()

