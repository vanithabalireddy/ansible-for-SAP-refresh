#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh
from ansible.module_utils.PostSystemRefresh import PostSystemRefresh


# For setting users to Administer Lock and Unlock
def bapi_user_lock(module, prefresh, params):
    data = dict()

    try:
        if params['fetch'] == 'users':
            user_list = prefresh.users_list()
            data["Entire System User List"] = user_list

        if params['fetch'] == 'locked_users':
            existing_locked_users = prefresh.existing_locked_users()
            data["User's who's status is already set to Administer Lock"] = existing_locked_users

        module.exit_json(changed=True, meta=data)

    except KeyError:
        if params['lock_users']['action'] == 'lock':
            user_list = prefresh.users_list()
            existing_locked_users = prefresh.existing_locked_users()
            exception_list = params['lock_users']['exception_list']

            active_users = [user for user in user_list if user not in existing_locked_users]

            locked_users, errors, excempted_users = prefresh.user_lock(active_users, exception_list, 'lock')

            data["Exception user list provided to keep them from locking"] = exception_list
            data["User's Locked with exception to the Exception user list provided ^^"] = locked_users

            module.exit_json(changed=True, meta=data)

        if params['lock_users']['action'] == 'unlock':
            user_list = prefresh.users_list()
            exception_list = params['lock_users']['exception_list']

            locked_users, errors, excempted_users = prefresh.user_lock(user_list, exception_list, 'unlock')

            data["User's who's current status is set to Lock(*including existing users that are locked)"] = exception_list
            data["User's Unlocked with exception to the users who's status was already locked prior to the activity"] = locked_users

            module.exit_json(changed=True, meta=data)

    except Exception as e:
        data["Error"] = e
        module.exit_json(changed=False, meta=data)


def suspend_bg_jobs(module, prefresh, params):
    if params:
        response = prefresh.suspend_bg_jobs()
        module.exit_json(changed=True, meta={'stdout': response})


def export_printers(module, prefresh, params):
    if params:
        report = params['report']
        variant_name = params['variant_name']
        response = prefresh.export_printer_devices(report, variant_name)
        module.exit_json(changed=True, meta={'stdout': response})


def user_master_export(module, prefresh, params):
    if params['pc3_ctc_val']:
        response = prefresh.pc3_ctc_val()
        module.exit_json(changed=True, meta={'stdout': response})
    else:
        report = params['report']
        variant_name = params['variant_name']
        response = prefresh.user_master_export(report, variant_name)
        module.exit_json(changed=True, meta={'stdout': response})


def fetch(module, postrefresh, params):
    if params == 'bgd_val':
        response = postrefresh.check_background_jobs()
        module.exit_json(changed=True, meta={'stdout': response})


def del_old_bg_jobs(module, postrefresh, params):
    if params:
        report = params['report']
        variant_name = params['variant_name']
        response = postrefresh.del_old_bg_jobs(report, variant_name)
        module.exit_json(changed=True, meta={'stdout': response})


def main():
    fields = dict(
        bapi_user_lock=dict(
            fetch=dict(choices=['users', 'locked_users'], type='str'),
            lock_users=dict(action=dict(choices=['lock', 'unlock'], required=True),
                            exception_list=dict(required=True, type='list'), type='dict'),
            type='dict'),
        suspend_bg_jobs=dict(type='bool'),
        export_printers=dict(report=dict(required=True, type='str'),
                             variant_name=dict(required=True, type='str'), type='dict'),
        user_master_export=dict(report=dict(type='str'),
                                variant_name=dict(type='str'),
                                pc3_ctc_val=dict(default=True, type='bool'), type='dict'),
        fetch=dict(choices=['bgd_val'], type='str'),
        del_old_bg_jobs=dict(report=dict(required=True, type='str'),
                             variant_name=dict(required=True, type='str'), type='dict')
    )

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes": "CheckMode is not supported as of now!"})

    prefresh = PreSystemRefresh()
    postrefresh = PostSystemRefresh()

    if module.params['bapi_user_lock']:
        params = module.params['bapi_user_lock']
        bapi_user_lock(module, prefresh, params)

    if module.params['suspend_bg_jobs']:
        params = module.params['suspend_bg_jobs']
        suspend_bg_jobs(module, prefresh, params)

    if module.params['export_printers']:
        params = module.params['export_printers']
        export_printers(module, prefresh, params)

    if module.params['user_master_export']:
        params = module.params['user_master_export']
        user_master_export(module, prefresh, params)

    if module.params['fetch']:
        params = module.params['fetch']
        fetch(module, postrefresh, params)

    if module.params['del_old_bg_jobs']:
        params = module.params['del_old_bg_jobs']
        del_old_bg_jobs(module, postrefresh, params)


if __name__ == "__main__":
    main()
