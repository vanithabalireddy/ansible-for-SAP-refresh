from pyrfc import Connection
from configparser import ConfigParser
from ansible.module_utils.basic import *
import os
import logging


class PreSystemRefresh:
    data = dict()
    err = str()
    
    def __init__(self):
        self.config = ConfigParser()
        try:
            self.config.read(os.environ["HOME"] + '/.config/sap_config.ini')
            self.creds = self.config['SAP']

            logging.basicConfig(filename="/tmp/system_refresh.log", level=logging.INFO,
                                format='%(levelname)s: %(message)s: %(asctime)s')

            self.conn = Connection(user=self.creds['user'], passwd=self.creds['passwd'], ashost=self.creds['ashost'],
                                   sysnr=self.creds['sysnr'], sid=self.creds['sid'], client=self.creds['client'])
        except KeyError:
            self.config.read(os.path.expanduser('~') + '\.config\sap_config.ini')
            self.creds = self.config['SAP']

            logging.basicConfig(filename=os.path.expanduser('~') + '\system_refresh.log', level=logging.INFO,
                                format='%(levelname)s: %(message)s: %(asctime)s')

            self.conn = Connection(user=self.creds['user'], passwd=self.creds['passwd'], ashost=self.creds['ashost'],
                                   sysnr=self.creds['sysnr'], sid=self.creds['sid'], client=self.creds['client'])

        except Exception as e:
            logging.error("CONNECTION: Failed to connect to SAP. Please check the creds: {}".format(e))
