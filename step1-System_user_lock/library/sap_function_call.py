#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh


def bapi_user_lock(module, systemRefresh, params):

    user_list = None
    existing_locked_users = None
    locked_users = None

    exception_list = params['lock_users']['exception_list']

    data = dict()

    if params['user_list']:
        user_list = systemRefresh.users_list()
        data["Entire System User List"] = user_list

    if params['existing_locked_users']:
        existing_locked_users = systemRefresh.existing_locked_users()
        data["User's who's status is already set to Administer Lock"] = existing_locked_users

    if params['lock_users']['action'] == 'lock':
        list = [user for user in user_list if user not in existing_locked_users]
        locked_users, errors, excempted_users = systemRefresh.user_lock(list, exception_list, 'lock')
        data["Exception user list provided to keep them from locking"] = exception_list
        data["User's Locked with exception to the Exception user list provided ^^"] = locked_users

    if params['lock_users']['action'] == 'unlock':
        locked_users, errors, excempted_users = systemRefresh.user_lock(user_list, exception_list, 'unlock')
        data["User's who's current status is set to Lock(*including existing users that are locked)"] = exception_list
        data["User's Unlocked with exception to the users who's status was already locked prior to the activity"] = locked_users

    module.exit_json(changed=True, meta=data)


def main():
    fields = dict(
        bapi_user_lock=dict(
            user_list=dict(default=True, type='bool', required=True),
            existing_locked_users=dict(default=True, type='bool'),
            lock_users=dict(action=dict(choices=['lock', 'unlock'], required=True),
                            exception_list=dict(required=True, type='list'), default=True, type='dict'),
            type='dict')
    )

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes": "CheckMode is not supported as of now!"})

    systemRefresh = PreSystemRefresh()

    if module.params['bapi_user_lock']:
        params = module.params['bapi_user_lock']
        bapi_user_lock(module, systemRefresh, params)


if __name__ == "__main__":
    main()
