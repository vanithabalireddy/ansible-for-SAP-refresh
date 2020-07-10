from pyrfc import Connection
from configparser import ConfigParser
from ansible.module_utils.basic import *
import os


def main():
    self.config = ConfigParser()
    try:
        self.config.read(os.environ["HOME"] + '/.config/sap_config.ini')
        self.creds = self.config['SAP']

        self.conn = Connection(user=self.creds['user'], passwd=self.creds['passwd'], ashost=self.creds['ashost'],
                               sysnr=self.creds['sysnr'], sid=self.creds['sid'], client=self.creds['client'])

        if self.conn:
            return True
    except KeyError:
        self.config.read(os.path.expanduser('~') + '\.config\sap_config.ini')
        self.creds = self.config['SAP']

        self.conn = Connection(user=self.creds['user'], passwd=self.creds['passwd'], ashost=self.creds['ashost'],
                               sysnr=self.creds['sysnr'], sid=self.creds['sid'], client=self.creds['client'])

        if self.conn:
            return True
    except Exception:
        return False

    return False

if __name__ == '__main__':
    main()

