# -*- coding: utf-8 -*-
"""
Migrate some translations from files found in the GSA/sdg-indicators repository.
These files/folders are expected:
temp/en/sdg_goals.csv
temp/en/sdg_indicator_metadata.csv
temp/es/sdg_goals.csv
temp/es/sdg_indicator_metadata.csv
temp/fr/sdg_goals.csv
(french translation of indicator metadata not yet available)
"""

import os.path
import csv
import yaml

def export_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

def main():
    # First the goal metadata.
    for language in ['en', 'es', 'fr']:
        filename = os.path.join('temp', language, 'sdg_goals.csv')
        data = {}
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                data[row[0]] = {
                    'title': row[1].strip(),
                    'short': row[2].strip()
                }
        export_yaml(data, os.path.join('translations', language, 'global_goals.yml'))

    # Next the indicator and target metadata. No french yet.
    for language in ['en', 'es']:
        filename = os.path.join('temp', language, 'sdg_indicator_metadata.csv')
        indicator_data = {}
        target_data = {}
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                indicator_data[row[6]] = {
                    'title': row[7].strip()
                }
                target_data[row[0]] = {
                    'title': row[5].strip()
                }
        export_yaml(indicator_data, os.path.join('translations', language, 'global_indicators.yml'))
        export_yaml(target_data, os.path.join('translations', language, 'global_targets.yml'))

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
    main()