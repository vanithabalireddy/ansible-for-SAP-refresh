from pyrfc import Connection
from configparser import ConfigParser
from ansible.module_utils.basic import *
import os


class PreSystemRefresh:
    data = dict()
    err = str()

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(os.environ["HOME"] + '/.config/sap_config.cnf')
        self.creds = self.config['SAP']

        try:
            self.conn = Connection(user=self.creds['user'], passwd=self.creds['passwd'], ashost=self.creds['ashost'],
                                   sysnr=self.creds['sysnr'], sid=self.creds['sid'], client=self.creds['client'])
        except Exception as e:
            self.err = "Failed when connecting to SAP application, please check the creds passed!"
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

    def users_list(self, module):
        users = []
        try:
            tables = self.conn.call("RFC_READ_TABLE", QUERY_TABLE='USR02', FIELDS=[{'FIELDNAME': 'BNAME'}])
            for data in tables['DATA']:
                for names in data.values():
                    users.append(names)
            self.data['USERS'] = users
            self.data['stdout'] = True
            module.exit_json(changed=True, meta=self.data)
        except Exception as e:
            self.err = "Failed to fetch user's list from USR02 table: {}".format(e)
            self.data['stdout'] = False
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

    def existing_locked_users(self, module):
        params = dict(
            PARAMETER='ISLOCKED',
            FIELD='LOCAL_LOCK',
            SIGN='I',
            OPTION='EQ',
            LOW='L'
        )
        try:
            user_list = self.conn.call("BAPI_USER_GETLIST", SELECTION_RANGE=[params])
            locked_user_list = []

            for user in user_list['USERLIST']:
                locked_user_list.append(user['USERNAME'])

            self.data['EXISTING_LOCKED_USERS'] = locked_user_list
            self.data['stdout'] = True
            module.exit_json(changed=True, meta=self.data)
        except Exception as e:
            self.err = "Failed to get existing locked user list: {}".format(e)
            self.data['stdout'] = False
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

    def fetch_users(self):
        try:
            tables = self.conn.call("RFC_READ_TABLE", QUERY_TABLE='USR02', FIELDS=[{'FIELDNAME': 'BNAME'}])
        except Exception as e:
            return None

        users = []

        for data in tables['DATA']:
            for names in data.values():
                users.append(names)

        return users

    def bapi_user_lock(self, module, params):
        users_list = self.fetch_users()
        users_locked = []
        errors = dict()
        users_exempted = []
        if users_list:
            for user in users_list:
                if user not in params['EXCEPTION_USERS']:
                    try:
                        self.conn.call('BAPI_USER_LOCK', USERNAME=user)
                        users_locked.append(user)
                    except Exception as e:
                        errors[user] = e
                        pass
                else:
                    users_exempted.append(user)
        else:
            self.err = "Failed to get entire user list before locking users: {}".format(e)
            self.data['stdout'] = False
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

        self.data['USERS_LOCKED'] = users_locked
        self.data['ERRORS'] = errors
        self.data['EXCEPTION_USERS'] = users_exempted

        module.exit_json(changed=True, meta=self.data)

    def bapi_user_unlock(self, module, params):
        users_list = self.fetch_users()
        users_locked = []
        errors = dict()
        users_exempted = []
        if users_list:
            for user in users_list:
                if user not in params['EXCEPTION_USERS']:
                    try:
                        self.conn.call('BAPI_USER_UNLOCK', USERNAME=user)
                        users_locked.append(user)
                    except Exception as e:
                        errors[user] = e
                        pass
                else:
                    users_exempted.append(user)
        else:
            self.err = "Failed to get entire user list before unlocking the users: {}".format(e)
            self.data['stdout'] = False
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

        self.data['USERS_UNLOCKED'] = users_locked
        self.data['ERRORS'] = errors
        self.data['EXCEPTION_USERS'] = users_exempted

        module.exit_json(changed=True, meta=self.data)

    def inst_execute_report(self, module, params):
        try:
            self.conn.call("INST_EXECUTE_REPORT", PROGRAM=params['PROGRAM'])
            if params['PROGRAM'] == 'BTCTRNS1':
                self.data["Success"] = "Background Jobs are Suspended!"
            module.exit_json(changed=True, meta=self.data)
        except Exception as e:
            if params['PROGRAM'] == 'BTCTRNS1':
                self.err = "Failed to Suspend Background Jobs"
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

    def start_report_in_batch(self, module, params):
        try:
            self.conn.call("SUBST_START_REPORT_IN_BATCH", IV_JOBNAME=params['IV_JOBNAME'],
                           IV_REPNAME=params['IV_REPNAME'], IV_VARNAME=params['IV_VARNAME'])
            if params['IV_REPNAME'] == 'RSPOXDEV':
                self.data['Success'] = "Printer devices are Successfully exported!"
            if params['IV_REPNAME'] == 'ZRSCLXCOP':
                self.data['Success'] = "User Master Export is Successfully Completed!"
            module.exit_json(changed=True, meta=self.data)
        except Exception as e:
            if params['IV_REPNAME'] == 'RSPOXDEV':
                self.err = "Failed to Export Printer devices"
            if params['IV_REPNAME'] == 'ZRSCLXCOP':
                self.err = "User Master Export is Failed!"
            module.fail_json(msg=self.err, Error=to_native(e), exception=traceback.format_exc())

    def export_sys_tables_comm_insert(self, module, params):
        args = dict(
            NAME=params['NAME'],
            OPSYSTEM=params['OPSYSTEM'],
            OPCOMMAND=params['OPCOMMAND'],
            PARAMETERS=params['PARAMETERS']
        )

        try:
            self.conn.call("ZSXPG_COMMAND_INSERT", COMMAND=args)
            self.data["Success!"] = "Successfully inserted command {}".format(params['NAME'])
            module.exit_json(changed=True, meta=self.data)
        except Exception as e:
            self.err = "Failed to insert command {}".format(params['NAME'])
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

    def export_sys_tables_comm_execute(self, module, params):
        try:
            self.conn.call("SXPG_COMMAND_EXECUTE", COMMANDNAME=params['NAME'])
            self.data["Success!"] = "Successfully Executed command {} and exported system tables".format(params['NAME'])
            module.exit_json(changed=True, meta=self.data)
        except Exception as e:
            self.err = "Failed to Execute command {}".format(params['NAME'])
            module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

    def fetch(self, module, params):
        if params == 'sys_params':
            try:
                output = self.conn.call("RFC_READ_TABLE",
                                        QUERY_TABLE='E070L')  # IF Condition check needs to be implemented
            except Exception as e:
                self.err = "Failed while querying E070L Table: {}".format(e)
                module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

            result = dict()
            trans_val = None
            for data in output['DATA']:
                for val in data.values():
                    trans_val = ((val.split()[1][:3] + 'C') + str(int(val.split()[1][4:]) + 1))
                    result["trans_val"] = trans_val

            try:
                output = self.conn.call("RFC_READ_TABLE", QUERY_TABLE='TMSPCONF',
                                        FIELDS=[{'FIELDNAME': 'NAME'}, {'FIELDNAME': 'SYSNAME'},
                                                {'FIELDNAME': 'VALUE'}])
            except Exception as e:
                self.err = "Failed while fetching TMC CTC Value: {}".format(e)
                module.fail_json(msg=self.err, error=to_native(e), exception=traceback.format_exc())

            ctc = None
            for field in output['DATA']:
                if field['WA'].split()[0] == 'CTC' and field['WA'].split()[1] == self.creds['sid']:
                    ctc = field['WA'].split()[2]

            if ctc is '1':
                sid_ctc_val = self.creds['sid'] + '.' + self.creds['client']
                result["sid_ctc_val"] = sid_ctc_val
            else:
                sid_ctc_val = self.creds['sid']
                result["sid_ctc_val"] = sid_ctc_val

            result["client"] = self.creds['client']
            result["sid_val"] = self.creds['sid']

            if trans_val and ctc is not None:
                self.data['stdout'] = result
                module.exit_json(changed=True, meta=self.data)
            else:
                self.err = "Failed to fetch {}".format(params['sys_params'])
                module.fail_json(msg=self.err, error=to_native(), exception=traceback.format_exc())

    def check_variant(self, report, variant_name):
        try:
            output = self.conn.call("RS_VARIANT_CONTENTS_RFC", REPORT=report, VARIANT=variant_name)
        except Exception as e:
            return "Failed to check variant {}: {}".format(variant_name, e)

        var_content = []

        for key, value in output.items():
            if key == 'VALUTAB':
                var_content = value

        for cont in var_content:  # Export Printer devices
            if cont['SELNAME'] == 'FILE' and cont['LOW'] == '/tmp/printers':
                return True

        for cont in var_content:  # User Master Export
            if cont['SELNAME'] == 'COPYCLI' and cont['LOW'] == self.creds['client']:
                return True

        for cont in var_content:  # Delete_old_bg_jobs
            if cont['SELNAME'] == 'FORCE' and cont['LOW'] == 'X':
                return True

        for cont in var_content:  # Delete_outbound_queues_SMQ1
            if cont['SELNAME'] == 'DISPLAY' and cont['LOW'] == 'X':
                return True

        for cont in var_content:  # Delete_outbound_queues_SMQ2
            if cont['SELNAME'] == 'SET_EXEC' and cont['LOW'] == 'X':
                return True

        return False

    def create_variant(self, report, variant_name, desc, content, text, screen):
        try:
            self.conn.call("RS_CREATE_VARIANT_RFC", CURR_REPORT=report, CURR_VARIANT=variant_name, VARI_DESC=desc,
                           VARI_CONTENTS=content, VARI_TEXT=text, VSCREENS=screen)
        except Exception as e:
            return "Variant {} for report {} Creation is Failed! : {}".format(variant_name, report, e)

        if self.check_variant(report, variant_name) is True:
            return "Variant {} Successfully Created for report {}".format(variant_name, report)
        else:
            return "Creation of variant {} for report {} is Failed!!".format(variant_name, report)

    def delete_variant(self, report, variant_name):
        try:
            self.conn.call("RS_VARIANT_DELETE_RFC", REPORT=report, VARIANT=variant_name)
        except Exception as e:
            return "Deletion of variant {} of report {} is Failed!: {}".format(variant_name, report, e)

        if self.check_variant(report, variant_name) is False:
            return "Variant {} for report {} is Successfully Deleted".format(variant_name, report)
        else:
            return "Failed to delete variant {} for report {}".format(variant_name, report)

# 1. System user lock               = Done
# 2. Suspend background Jobs        = Done
# 3. Export Quality System Tables   = Not Done # Funciton module is not callable
# 4. Export Printer Devices         = Done     # SSH to fetch /tmp/printers file from target to ansible controller node.
# 5. User Master Export             = Done     # SSH to fetch user master exported file.

