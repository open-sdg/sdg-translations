# -*- coding: utf-8 -*-
"""
Future place for validating the translations.
"""

import os
import yaml

def require_full_coverage():
    """Make sure that no languages are missing translations."""

    # First we compile a full list of ALL translation keys.
    all_keys = {}
    for root, dirs, files in os.walk('translations'):
        language = os.path.basename(root)
        if (language == 'translations'):
            continue
        for filename in files:
            file_parts = os.path.splitext(filename)
            no_extension = file_parts[0]
            extension = file_parts[1]
            if (extension == '.yml'):
                with open(os.path.join(root, filename), 'r') as stream:
                    try:
                        yamldata = (yaml.load(stream, Loader=yaml.FullLoader))
                        if filename not in all_keys:
                            all_keys[filename] = {}
                        for key in yamldata:
                            all_keys[filename][key] = True
                    except Exception as exc:
                        print (exc)

    # Now we go again, this time looking for missing keys.
    errors = []
    for root, dirs, files in os.walk('translations'):
        language = os.path.basename(root)
        if (language == 'translations'):
            continue
        for filename in files:
            filepath = os.path.join(root, filename)
            if not os.path.isfile(filepath):
                raise Exception('Missing translation file: ' + filepath)
            with open(filepath, 'r') as stream:
                yamldata = (yaml.load(stream, Loader=yaml.FullLoader))
                for required_key in all_keys[filename]:
                    if required_key not in yamldata:
                        errors.append('Missing key "' + required_key + '" in file: ' + filepath)

    if len(errors) > 0:
        for error in errors:
            print(error)
        raise Exception('Failed test for full coverage because keys were missing.')


def main():
    require_full_coverage()


if __name__ == '__main__':
    main()
