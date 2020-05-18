#!/usr/bin/python

report = "{{ report }}"
variant_name = "{{ variant_name }}"
client = "{{ client }}"

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

text = [{'MANDT': "100", 'LANGU': 'EN', 'REPORT': report, 'VARIANT': variant_name, 'VTEXT': 'Printers Export'}]

screen = [{'DYNNR': '1000', 'KIND': 'P'}]

