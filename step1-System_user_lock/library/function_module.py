#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh


def user_list():
    pass


def main():
    fields = dict(
        user_list=dict(
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

    systemRefresh = PreSystemRefresh()

    user_list = None
    if module.params['user_list']:
        action = module.params['user_list']['action']
        if action == True:
            user_list = systemRefresh.users_list()

    result = user_list
    data = {"Result": result}

    module.exit_json(changed=True, meta=data)


if __name__ == "__main__":
    main()
