# -*- coding: utf-8 -*-
"""
Convert the YAML context files into a single JSON file.
"""

import os
import yaml
import json
import shutil

def build_contexts():
    status = True
    data = []

    for root, dirs, files in os.walk('contexts'):
        for file in files:
            file_parts = os.path.splitext(file)
            no_extension = file_parts[0]
            extension = file_parts[1]
            if (extension == '.yml'):
                with open(os.path.join(root, file), 'r') as stream:
                    try:
                        yamldata = (yaml.load(stream))
                        for key in yamldata:
                            context_key = no_extension + ':' + key
                            data.append({
                                "key": context_key,
                                "context": yamldata[key]
                            })
                    except Exception as exc:
                        print (exc)

    json_dir = 'www'
    if not os.path.exists(json_dir):
        os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, "contexts.json")
    with open(json_path, 'w') as fp:
        json.dump(data, fp, sort_keys=True)

    return status

def main():

    status = build_contexts()
    return status

if __name__ == '__main__':
    status = main()
    if(not status):
        raise RuntimeError("Failed contexts build")
    else:
        print("Success")
