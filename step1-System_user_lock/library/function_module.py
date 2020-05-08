#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh


def main():
    fields = dict(
        bapi_user_lock=dict(
            user_list=dict(default=True, type='bool'),
            existing_locked_users=dict(default=True, type='bool'),
            lock_users=dict(default=True, type='bool'),
            type='dict'),
    )

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes" : "CheckMode is not supported as of now!"})

    systemRefresh = PreSystemRefresh()

    user_list = None
    existing_locked_users = None
    locked_users = None
    exception_list = ['SST_TRNG', 'KRISHNA', 'BJOERN', 'DDIC', 'DMAGENDIRAN', 'GIRIDR', 'MRAM']

    if module.params['bapi_user_lock']:
        if module.params['bapi_user_lock']['user_list'] == True:
            user_list = systemRefresh.users_list()
        if module.params['bapi_user_lock']['existing_locked_users'] == True:
            existing_locked_users = systemRefresh.existing_locked_users()
        if module.params['bapi_user_lock']['locked_users'] == True:
            locked_users = systemRefresh.user_lock(user_list, exception_list, 'lock')

    data = dict()
    data['User_List'] = user_list
    data['Existing_locked_users'] = existing_locked_users
    data['Users_Locked'] = locked_users

    module.exit_json(changed=True, meta=data)


if __name__ == "__main__":
    main()
