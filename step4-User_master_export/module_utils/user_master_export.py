#!/usr/bin/python

report = "ZRSCLXCOP"
variant_name = "SST_ZUSR_EXP"

desc = dict(
    MANDT=self.creds['client'],
    REPORT=report,
    VARIANT=variant_name
)

content = [{'SELNAME': 'COPYCLI', 'KIND': 'P', 'LOW': self.creds['client']},
           {'SELNAME': 'SUSR', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'MODUS', 'KIND': 'P', 'LOW': 'E'},
           {'SELNAME': 'ALTINP', 'KIND': 'P', 'LOW': 'A'},
           {'SELNAME': 'COMFILE', 'KIND': 'P', 'LOW': 'PC3C900014'},
           {'SELNAME': 'PROF', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'PROFIL', 'KIND': 'P', 'LOW': 'SAP_USER'},
           {'SELNAME': 'TARGET', 'KIND': 'P', 'LOW': 'PC3'}]

text = [{'MANDT': self.creds['client'], 'LANGU': 'EN', 'REPORT': report, 'VARIANT': variant_name,
         'VTEXT': 'User Master Export'}]

screen = [{'DYNNR': '1000', 'KIND': 'P'}]

