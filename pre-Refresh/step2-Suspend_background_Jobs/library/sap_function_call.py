#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh


class SAPFunctionCall(PreSystemRefresh):

    def suspend_bg_jobs(self, module, params):
        data = dict()
        try:
            self.conn.call("INST_EXECUTE_REPORT", PROGRAM=params['PROGRAM'])
            data["Success!"] = "Background Jobs are Suspended!"
            module.exit_json(changed=True, meta=data)
        except Exception as e:
            data["Failure!"] = "Failed to Suspend Background Jobs: {}".format(e)
            module.exit_json(changed=False, meta=data)

    def export_sys_tables_comm_insert(self, module, params):
        data = dict()
        args = dict(
            NAME=params['NAME'],
            OPSYSTEM=params['OPSYSTEM'],
            OPCOMMAND=params['OPCOMMAND'],
            PARAMETERS=params['PARAMETERS']
        )

        try:
            self.conn.call("ZSXPG_COMMAND_INSERT", COMMAND=args)
            data["Success!"] = "Successfully inserted command {}".format(params['NAME'])
            module.exit_json(changed=True, meta=data)
        except Exception as e:
            data["Failure!"] = "Failed to insert command {} = {}".format(params['NAME'], e)
            module.exit_json(changed=False, meta=data)

    def export_sys_tables_comm_execute(self, module, params):
        command_name = params['NAME']
        data = dict()
        try:
            self.conn.call("SXPG_COMMAND_EXECUTE", COMMAND=command_name)
            data["Success!"] = "Successfully Executed command {} and exported system tables".format(params['NAME'])
            module.exit_json(changed=True, meta=data)
        except Exception as e:
            data["Failure!"] = "Failed to Execute command {} = {}".format(params['NAME'], e)
            module.exit_json(changed=False, meta=data)


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

            data[
                "User's who's current status is set to Lock(*including existing users that are locked)"] = exception_list
            data[
                "User's Unlocked with exception to the users who's status was already locked prior to the activity"] = locked_users

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


def main():
    fields = dict(
        bapi_user_lock=dict(
            fetch=dict(choices=['users', 'locked_users'], type='str'),
            lock_users=dict(action=dict(choices=['lock', 'unlock'], required=True),
                            exception_list=dict(required=True, type='list'), type='dict'),
            type='dict'),
        INST_EXECUTE_REPORT=dict(PROGRAM=dict(type='str'), type='dict'),
        suspend_bg_jobs=dict(type='bool'),
        export_printers=dict(report=dict(required=True, type='str'),
                             variant_name=dict(required=True, type='str'), type='dict'),
        user_master_export=dict(report=dict(type='str'),
                                variant_name=dict(type='str'),
                                pc3_ctc_val=dict(default=True, type='bool'), type='dict'),
        ZSXPG_COMMAND_INSERT=dict(NAME=dict(type='str'),
                                  OPSYSTEM=dict(type='str'),
                                  OPCOMMAND=dict(type='str'),
                                  PARAMETERS=dict(type='str'), type='dict'),
        SXPG_COMMAND_EXECUTE=dict(COMMAND=dict(type='str'), type='dict')

    )

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes": "CheckMode is not supported as of now!"})

    prefresh = PreSystemRefresh()
    functioncall = SAPFunctionCall()

    if module.params['bapi_user_lock']:
        params = module.params['bapi_user_lock']
        bapi_user_lock(module, prefresh, params)

    if module.params['INST_EXECUTE_REPORT']:
        params = module.params['INST_EXECUTE_REPORT']
        functioncall.suspend_bg_jobs(module, params)

    if module.params['export_printers']:
        params = module.params['export_printers']
        export_printers(module, prefresh, params)

    if module.params['user_master_export']:
        params = module.params['user_master_export']
        user_master_export(module, prefresh, params)

    if module.params['ZSXPG_COMMAND_INSERT']:
        params = module.params['ZSXPG_COMMAND_INSERT']
        functioncall.export_sys_tables_comm_insert(module, params)

    if module.params['SXPG_COMMAND_EXECUTE']:
        params = module.params['SXPG_COMMAND_EXECUTE']
        functioncall.export_sys_tables_comm_execute(module, params)


if __name__ == "__main__":
    main()
