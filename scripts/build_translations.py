# -*- coding: utf-8 -*-
"""
Convert the YAML translation files into a single JSON file.
"""

import os
import yaml
import json

def main():
    status = True

    data = {}

    for root, dirs, files in os.walk('translations'):
        key = os.path.basename(root)
        if (key == 'translations'):
            continue
        data[key] = {}
        for file in files:
            file_parts = os.path.splitext(file)
            no_extension = file_parts[0]
            extension = file_parts[1]
            if (extension == '.yml'):
                with open(os.path.join(root, file), 'r') as stream:
                    try:
                        yamldata = (yaml.load(stream))
                        data[key][no_extension] = yamldata
                    except Exception as exc:
                        print (exc)

    json_dir = '_site'
    if not os.path.exists(json_dir):
        os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, 'translations.json')
    with open(json_path, 'w') as fp:
        json.dump(data, fp)

    return status

if __name__ == '__main__':
    status = main()
    if(not status):
        raise RuntimeError("Failed translation build")
    else:
        print("Success")
