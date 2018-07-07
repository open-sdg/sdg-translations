# -*- coding: utf-8 -*-
"""
Migrate metadata keys from schema in the ONSdigital/sdg-data repository.
"""

import os.path
import json
import requests
import yaml

def export_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

def main():
    url = 'https://onsdigital.github.io/sdg-data/meta/schema.json'
    data = {}
    response = json.loads(requests.get(url).text)
    scopes = [
        'global',
        'national',
        'source_1',
        'source_2',
        'source_3',
        'source_4',
        'source_5',
        'source_6',
    ]
    for language in ['en', 'es', 'fr']:
        for row in response:
            if 'scope' in row['field']:
                if row['field']['scope'] not in scopes:
                    continue
                if '_link_text' in row['name'] or '_url_text' in row['name']:
                    continue
                if language == 'en':
                    data[row['name']] = row['field']['label']
                else:
                    data[row['name']] = 'Needs translation'

        export_yaml(data, os.path.join('translations', language, 'metadata_fields.yml'))

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
    main()