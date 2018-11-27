# -*- coding: utf-8 -*-
"""
Export all translation keys to a CSV file for easy translation.
"""

import os
import yaml
import pandas as pd
import csv
import sys

# Decide if we actually want to export a particular key.
def should_we_omit_key(key, language):

    # Ignore keys that start with and end with these values.
    starts_with_and_ends_with = [
        # No need to translate URLs.
        ('global_indicators', 'metadata_link'),
        # No need to translate organisation names.
        ('global_indicators', 'custodian_agency'),
        # For now let's leave off the "Definition" as well, only because it
        # would be a significant translation effort, and we may want to find out
        # whether the UN may eventually do this translation.
        ('global_indicators', 'definition'),
    ]
    # Add some more for offical UN languages.
    official_un_languages = ['es', 'fr', 'zh-Hans']
    if language in official_un_languages:
        starts_with_and_ends_with.extend([
            # The titles for these are pulled directly from UN sources.
            ('global_indicators', 'title'),
            ('global_targets', 'title'),
            ('global_goals', 'title'),
        ])
    # Ignore keys that start with these values.
    starts_with = [
        # This key is identical in all languages.
        'languages'
    ]

    # Now do the actual ignoring.
    for item in starts_with_and_ends_with:
        if key.startswith(item[0]) and key.endswith(item[1]):
            return True
    for item in starts_with:
        if key.startswith(item):
            return True

    # Still here? It must be fine.
    return False

# Parse and "flatten" the yaml from a translation file.
def parse_translation_data(filepath):
    with open(filepath, 'r') as stream:
        try:
            yamldata = yaml.load(stream)
            # Use an unusual "sep" below so that dots can still be used in keys.
            df = pd.io.json.json_normalize(yamldata, sep='---')
            return df.to_dict(orient='records')[0]
        except Exception as exc:
            # Could not load the file, return an empty object.
            return {}

def export_language(language, folder):
    src_language = 'en'
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
                full_key = no_extension + ':' + key
                # First make sure we shouldn't ignore this one.
                if should_we_omit_key(full_key, language):
                    continue
                rows.append({
                    # First column is a combination of the filename and the
                    # "flattened" key, separated by a colon. For example:
                    # frontpage:disclaimer_text
                    'key': full_key,
                    # Second column is the source language - English.
                    src_language: src_data[key],
                    # Third column is the destination language, if it exists.
                    language: dest_data[key] if key in dest_data else ''
                })
    keys = rows[0].keys()

    # Write our results to a file.
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    csv_filename = 'sdg-translations-' + language + '.csv'
    csv_filepath = os.path.join(folder, csv_filename)
    with open(csv_filepath, 'w', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rows)

def main():

    # Abort if there is no parameter provided.
    if len(sys.argv) < 2:
        sys.exit('Provide a 2-letter abbreviation for the target language.')
    language = sys.argv[1]
    export_language(language, '.')

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
    main()
