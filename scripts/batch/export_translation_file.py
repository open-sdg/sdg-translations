# -*- coding: utf-8 -*-
"""
Export all translation keys to a CSV file for easy translation.
"""

import os
import yaml
import pandas as pd
import csv
import sys

def main():

    if len(sys.argv) < 1:
        sys.exit('Provide a 2-letter abbreviation for the target language.')

    language = sys.argv[1]
    rows = []
    english = os.path.join('translations', 'en')

    for filename in os.listdir(english):
        file_parts = os.path.splitext(filename)
        no_extension = file_parts[0]
        extension = file_parts[1]
        if extension == '.yml':
            filepath = os.path.join(english, filename)
            with open(filepath, 'r') as stream:
                try:
                    yamldata = yaml.load(stream)
                    df = pd.io.json.json_normalize(yamldata)
                    flattened = df.to_dict(orient='records')[0]
                    for key in flattened:
                        rows.append({
                            'key': no_extension + ':' + key,
                            'en': flattened[key],
                            language: ''
                        })
                except Exception as exc:
                    print(exc)
    keys = rows[0].keys()

    csv_filename = 'sdg_translations_' + language + '.csv'
    with open(csv_filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rows)

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
    main()