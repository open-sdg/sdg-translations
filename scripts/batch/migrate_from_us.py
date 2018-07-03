# -*- coding: utf-8 -*-
"""
Migrate some translations from files found in the GSA/sdg-indicators repository.
"""

import os.path
import csv
import urllib.request
import codecs
import yaml

def remote_url(language, filename):
  prefix = 'https://gsa.github.io/sdg-indicators/data/'
  if language == 'en':
    return prefix + filename
  else:
    return prefix + language + '/' + filename

def export_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

def main():
    # First the goal metadata.
    for language in ['en', 'es', 'fr']:
        url = remote_url(language, 'sdg_goals.csv')
        data = {}
        stream = urllib.request.urlopen(url)
        reader = csv.reader(codecs.iterdecode(stream, 'utf-8'))
        next(reader)
        for row in reader:
            data[row[0]] = {
                'title': row[1].strip(),
                'short': row[2].strip()
            }
        export_yaml(data, os.path.join('translations', language, 'global_goals.yml'))

    # Next the indicator and target metadata. No french yet.
    for language in ['en', 'es']:
        url = remote_url(language, 'sdg_indicator_metadata.csv')
        indicator_data = {}
        target_data = {}
        stream = urllib.request.urlopen(url)
        reader = csv.reader(codecs.iterdecode(stream, 'utf-8'))
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