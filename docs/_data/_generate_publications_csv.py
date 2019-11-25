#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate "publications.csv" file for the publication page.
Author: Yao-Yuan Mao
Usage: ./_generate_publications_csv.py
Reproduced with permission from: https://github.com/LSSTDESC/lsstdesc.github.io/blob/master/_data/_generate_publications_csv.py
Note:
- Require ads (pip install ads) https://pypi.org/project/ads/
- Need to set up ADS_DEV_KEY (see https://ads.readthedocs.io/)
- Edit MANUAL_ADDITION and NON_JOURNAL_ENTRIES as needed
"""

from __future__ import unicode_literals
import sys
import json
import csv
if sys.version_info[0] < 3:
    from backports import csv
    from io import open
from io import StringIO
import ads

MANUAL_ADDITION = [
    '2019JCAP...10..035H',
    '2019arXiv190805276D',
    '2019arXiv190104454S',
    '2018JCAP...11..009D',
    '2018JCAP...10..028M',
    '2018JCAP...07..043F',
    '2017JCAP...12..009S',
]

NON_JOURNAL_ENTRIES = [
]

NON_JOURNAL_BIBSTEM = ['BAAS']

MANUAL_EXCLUSION = []
EXCLUDED_BIBSTEM = ['AAS', 'ehep.conf']

def fix_csv_header(header_line):
    header_line = header_line.replace('"author"', '"authors"')
    header_line = header_line.replace('"pubdate"', '"date"')
    header_line = header_line.replace('"page,page_range"', '"page"')
    header_line = header_line.replace('"pub"', '"journal"')
    header_line = header_line.replace('"eid,identifier"', '"arxiv"')
    header_line += ',"type"'
    return header_line

def retrieve_csv_from_ads(bibcodes):
    export_service = ads.ExportQuery(bibcodes)
    export_service.format = 'custom'
    export_service.json_payload = json.dumps({
        'bibcode': bibcodes,
        'format': '%ZEncoding:csv %R %D %T %L %Y %q %V %p %X %d"journal-paper"\n'
    })
    header, _, content = export_service.execute().partition('\n')
    return fix_csv_header(header) + '\n' + content

def apply_row_fixes(row, non_journal_entries=tuple(NON_JOURNAL_ENTRIES),
                    non_journal_bibstem=tuple(NON_JOURNAL_BIBSTEM)):
    if row['journal'] in non_journal_bibstem or row['bibcode'] in non_journal_entries:
        row['type'] = 'non-journal'
    return row

def update_and_write_csv(csv_text, output_path='publications.csv'):
    reader = csv.DictReader(StringIO(csv_text))
    with open(output_path, 'w') as output:
        writer = csv.DictWriter(output, fieldnames=reader.fieldnames,
                                lineterminator='\n')
        writer.writeheader()
        for row in reader:
            writer.writerow(apply_row_fixes(row))

def main():
    bibcodes = list(MANUAL_ADDITION)
    update_and_write_csv(retrieve_csv_from_ads(bibcodes))

if __name__ == '__main__':
    main()
