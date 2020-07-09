import
client= {{ lookup('ini', 'client section=SAP file={{ ansible_env.HOME }}/.config/sap_config.ini') }}
file= '/tmp/exp_qa_all.dat'