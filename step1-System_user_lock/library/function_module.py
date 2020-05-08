#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh


def main():
    fields = dict(
        users_list=dict(
            action=dict(default=True, type='bool'),
            type='dict'),
        existing_locked_users=dict(
            action=dict(default=True, type='bool'),
            type='dict'),
        lock_users=dict(
            action=dict(default=True, type='bool'),
            type='dict')
    )

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes" : "CheckMode is not supported as of now!"})

    users_list = module.params['users_list']

    result = users_list
    data = {"Result": result}

    module.exit_json(changed=True, meta=data)


if __name__ == "__main__":
    main()
