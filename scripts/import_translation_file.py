# -*- coding: utf-8 -*-
"""
Import translation values from a previously exported (and then edited) CSV file.
"""

import os
import yaml
import pandas as pd
import csv
import sys
from unflatten import unflatten

def change_keys(obj, convert):
    """
    Recursively goes through the dictionary obj and replaces keys with the convert function.
    """
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            new[convert(k)] = change_keys(v, convert)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(change_keys(v, convert) for v in obj)
    else:
        return obj

    return new

def merge_dicts(source, destination):
    """
    Recursively merge the values in the source dict onto the destination dict.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination

def main():

    if len(sys.argv) < 2:
        sys.exit('Provide the path to the exported CSV file you would like to import.')

    export_path = sys.argv[1]
    with open(export_path, 'r') as csvfile:
        data = csv.reader(csvfile)
        header = next(data)
        language = header[2]
        if len(header) < 2:
            sys.exit('The header for the third column must be a language code.')
        # Make sure the folder exists.
        language_folder = os.path.join('translations', language)
        if not os.path.isdir(language_folder):
            os.mkdir(language_folder)

        yaml_files = {}

        for row in data:
            key_string = row[0]
            key_parts = key_string.split(':')
            filename = key_parts[0]
            key_flat = key_parts[1]

            # For now replace dots with something recognizable that we can
            # replace later. This is because dots mess up the "unflatten"
            # library.
            key_flat = key_flat.replace('.', '^^^')

            # Along the same lines, we now put dots where we actually want dots.
            # The export script uses a separation string of "---" instead of
            # dots, so now let's replace those, to prepare for unflattening.
            key_flat = key_flat.replace('---', '.')

            translation = row[2]

            if filename not in yaml_files:
                # Start with an empty dict.
                yaml_files[filename] = {}
                # But also check to see if there is existing data.
                filepath = os.path.join(language_folder, filename + '.yml')
                if (os.path.isfile(filepath)):
                    with open(filepath, 'r') as infile:
                        existing = yaml.load(infile)
                        if existing:
                            yaml_files[filename] = existing

            # Unflatted and merge the data into our yaml_files dict.
            unflattened = unflatten({key_flat: translation})
            yaml_files[filename] = merge_dicts(unflattened, yaml_files[filename])

        # Put the dots back into the keys.
        yaml_files = change_keys(yaml_files, lambda key: key.replace('^^^', '.'))

        # Loop through the yaml_files dict and write any changes to file.
        for yaml_file in yaml_files:
            yaml_path = os.path.join(language_folder, yaml_file + '.yml')
            with open(yaml_path, 'w') as outfile:
                yaml.dump(yaml_files[yaml_file], outfile, default_flow_style=False, allow_unicode=True)

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
    main()