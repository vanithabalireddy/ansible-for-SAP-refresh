#!/usr/bin/python

report = "RSPOXDEV"
variant_name = "SST_ZPRINT_EXP"
client = "100"

desc = dict(
    MANDT=client,
    REPORT=report,
    VARIANT=variant_name
)

content = [{'SELNAME': 'DO_SRV', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': '_EXP', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'DO_EXP', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'DO_LOG', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'WITH_CNF', 'KIND': 'P', 'LOW': 'X'},
           {'SELNAME': 'DEVICE', 'KIND': 'S', 'SIGN': 'I', 'OPTION': 'CP', 'LOW': '*'},
           {'SELNAME': 'FILE', 'KIND': 'P', 'LOW': '/tmp/printers'}]

text = [{'MANDT': client, 'LANGU': 'EN', 'REPORT': report, 'VARIANT': variant_name, 'VTEXT': 'Printers Export'}]

screen = [{'DYNNR': '1000', 'KIND': 'P'}]

