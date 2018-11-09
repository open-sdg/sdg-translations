---
layout: page
title: Developers
---

The translations are compiled and available at:

{{ site.url }}{{ site.baseurl }}/translations.json

## Previous releases

Each past release is available separately, according to its tag. For example, release 0.1.0 is available at:

{{ site.url }}{{ site.baseurl }}/translations-0.1.0.json

## Importing spreadsheets from translators

An exported spreadsheet can be re-imported back into the repository, after having been edited, by running a Python script, and specifying a path to the file:

`python scripts/import_translation_file /path/to/my-translation-file.csv`

Note that this only updates the .yml files, but it is still up to you to use Git to commit the changes and create a pull-request.