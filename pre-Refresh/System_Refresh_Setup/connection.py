from pyrfc import Connection
from configparser import ConfigParser
import os


def main():
    config = ConfigParser()
    try:
        config.read(os.environ["HOME"] + '/.config/{}.ini'.format(os.environ["HOSTNAME"]))
        creds = config['SAP']

        Connection(user=creds['user'], passwd=creds['passwd'], ashost=creds['ashost'],
                               sysnr=creds['sysnr'], sid=creds['sid'], client=creds['client'])

        return True
    except KeyError:
         config.read(os.path.expanduser('~') + '\.config\{}.ini'.format(os.environ['COMPUTERNAME']))
         creds = config['SAP']

         Connection(user=creds['user'], passwd=creds['passwd'], ashost= creds['ashost'],
                           sysnr=creds['sysnr'], sid=creds['sid'], client=creds['client'])

         return True
    except Exception:
        return False


if __name__ == '__main__':
    print(main())

