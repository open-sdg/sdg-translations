# -*- coding: utf-8 -*-
"""
Export all translation keys to a CSV file for easy translation.
"""

import os
import yaml
import pandas as pd
import csv
import sys

# Parse and "flatten" the yaml from a translation file.
def parse_translation_data(filepath):
    with open(filepath, 'r') as stream:
        try:
            yamldata = yaml.load(stream)
            # Use an unusual "sep" below so that dots can still be used in keys.
            df = pd.io.json.json_normalize(yamldata, sep='---')
            return df.to_dict(orient='records')[0]
        except Exception as exc:
            print(exc)

def main():

    # Abort if there is no parameter provided.
    if len(sys.argv) < 2:
        sys.exit('Provide a 2-letter abbreviation for the target language.')

    src_language = 'en'
    language = sys.argv[1]
    rows = []
    src = os.path.join('translations', src_language)
    dest = os.path.join('translations', language)
    # A flag to remember whether a translation already exists or not.
    translation_exists = os.path.isdir(dest)

    # Loop through the translation files in the source language.
    for filename in os.listdir(src):
        file_parts = os.path.splitext(filename)
        no_extension = file_parts[0]
        extension = file_parts[1]
        # Only operate on Yaml files.
        if extension == '.yml':
            src_filepath = os.path.join(src, filename)
            src_data = parse_translation_data(src_filepath)
            # If a translation does not exist, the third column will be blank.
            # But if a translation exists, we want to populate the third column
            # with the current translation.
            dest_data = {}
            if translation_exists:
                dest_filepath = os.path.join(dest, filename)
                dest_data = parse_translation_data(dest_filepath)
            # Loop through the source data and append rows for the CSV output.
            for key in src_data:
                rows.append({
                    # First column is a combination of the filename and the
                    # "flattened" key, separated by a colon. For example:
                    # frontpage:disclaimer_text
                    'key': no_extension + ':' + key,
                    # Second column is the source language - English.
                    src_language: src_data[key],
                    # Third column is the destination language, if it exists.
                    language: dest_data[key] if key in dest_data else ''
                })
    keys = rows[0].keys()

    # Write our results to a file.
    csv_filename = 'sdg_translations_' + language + '.csv'
    with open(csv_filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rows)

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
    main()