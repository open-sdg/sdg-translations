# -*- coding: utf-8 -*-
"""
Convert the YAML translation files into a single JSON file.
"""

import os
import yaml
import json
import shutil
from git import Repo

def build_translations(output_file):
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
                        yamldata = (yaml.load(stream, Loader=yaml.FullLoader))
                        data[key][no_extension] = yamldata
                    except Exception as exc:
                        print (exc)

    json_dir = 'www'
    if not os.path.exists(json_dir):
        os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, output_file)
    with open(json_path, 'w') as fp:
        json.dump(data, fp, sort_keys=True)

    return status

def main():
    status = True

    data = {}

    # First output the latest code.
    build_translations('translations.json')

    # Loop through all the past Git tags.
    repo = Repo(os.getcwd())
    # Save the current branch for later.
    try:
        print('Starting branch was ' + branch)
    except:
        branch = 'my-temporary-branch-that-is-hopefully-not-being-used'
        temp_branch = repo.create_head(branch)
        temp_branch.checkout()
    for tag in repo.tags:
        # Switch to the tag and build another version.
        repo.git.checkout(tag)
        build_translations('translations-' + str(tag) + '.json')
    # Go back to the current branch.
    if branch:
        repo.git.checkout(branch)

    return status

if __name__ == '__main__':
    status = main()
    if(not status):
        raise RuntimeError("Failed translation build")
    else:
        print("Success")
