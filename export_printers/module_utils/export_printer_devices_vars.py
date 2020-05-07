#!/usr/bin/python

report = "RSPOXDEV"
variant_name = "ZPRINT_EXP"

desc = dict(
    MANDT="100",
    REPORT="RSPOXDEV",
    VARIANT="ZPRINT_EXP"
)

content = [{'SELNAME': 'DO_SRV', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': '_EXP', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'DO_EXP', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'DO_LOG', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'WITH_CNF', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'DEVICE', 'KIND': 'S', 'SIGN': 'I', 'OPTION': 'CP', 'LOW': '*'},
           {'SELNAME': 'FILE', 'KIND': 'P', 'LOW': '/tmp/printers'}]

text = [{'MANDT': "100", 'LANGU': 'EN', 'REPORT': "RSPOXDEV", 'VARIANT': "ZPRINT_EXP", 'VTEXT': 'Printers Export'}]

screen = [{'DYNNR': '1000', 'KIND': 'P'}]

