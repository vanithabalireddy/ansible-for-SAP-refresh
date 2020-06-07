#!/usr/bin/python
from ansible.module_utils.basic import *
from ansible.module_utils.PreSystemRefresh import PreSystemRefresh
from ansible.module_utils.PostSystemRefresh import PostSystemRefresh


def main():
    fields = dict(
        FETCH=dict(
            choices=['sys_params', 'sys_users', 'sys_locked_users', 'bgd_val'], type='str'),
        BAPI_USER_LOCK=dict(
            EXCEPTION_USERS=dict(required=True, type='list'), type='dict'),
        BAPI_USER_UNLOCK=dict(
            EXCEPTION_USERS=dict(required=True, type='list'), type='dict'),
        INST_EXECUTE_REPORT=dict(
            PROGRAM=dict(required=True, type='str'), type='dict'),
        SUBST_START_REPORT_IN_BATCH=dict(
            IV_JOBNAME=dict(required=True, type='str'),
            IV_REPNAME=dict(required=True, type='str'),
            IV_VARNAME=dict(required=True, type='str'), type='dict')
    )

    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json({"Mes": "CheckMode is not supported as of now!"})

    prefresh = PreSystemRefresh()
    postRefresh = PostSystemRefresh()

    if module.params['FETCH']:
        params = module.params['FETCH']
        if params == 'sys_params':
            prefresh.fetch(module, params)
        if params == 'sys_users':
            prefresh.users_list(module)
        if params == 'sys_locked_users':
            prefresh.existing_locked_users(module)
        if params == 'bgd_val':
            postRefresh.check_bg_jobs(module)

    if module.params['BAPI_USER_LOCK']:
        params = module.params['BAPI_USER_LOCK']
        prefresh.bapi_user_lock(module, params)

    if module.params['BAPI_USER_UNLOCK']:
        params = module.params['BAPI_USER_UNLOCK']
        prefresh.bapi_user_unlock(module, params)

    if module.params['INST_EXECUTE_REPORT']:
        params = module.params['INST_EXECUTE_REPORT']
        postRefresh.inst_execute_report(module, params)

    if module.params['SUBST_START_REPORT_IN_BATCH']:
        params = module.params['SUBST_START_REPORT_IN_BATCH']
        postRefresh.start_report_in_batch(module, params)


if __name__ == "__main__":
    main()
