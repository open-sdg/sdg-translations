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

        yaml_files = {}

        for row in data:
            key_string = row[0]
            key_parts = key_string.split(':')
            filename = key_parts[0]
            key_flat = key_parts[1]
            translation = row[2]

            if filename not in yaml_files:
                yaml_files[filename] = {}

            unflattened = unflatten({key_flat: translation})
            yaml_files[filename] = {**yaml_files[filename], **unflattened}

        for yaml_file in yaml_files:
            yaml_path = os.path.join('translations', language, yaml_file + '.yml')
            with open(yaml_path, 'w') as outfile:
                yaml.dump(yaml_files[yaml_file], outfile, default_flow_style=False, allow_unicode=True)

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
    main()