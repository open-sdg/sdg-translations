# SDG Translations

This repository contains a set of translations of common words and phrases intended for use in the SDG National Reporting Platform.

The translations are compiled and available at:

http://brock.tips/sdg-translations/translations.json

## Previous releases

Each past release is available separately, according to its tag. For example, release 0.1.0 is available at:

http://brock.tips/sdg-translations/translations-0.1.0.json

## Exporting

A convenient spreadsheet can be created by running a Python script, and specifying a 2-letter language code, like "es":

`python scripts/batch/export_translation_file es`

That command would export a spreadsheet with the English translations alongside the Spanish (es) translations. If there were no Spanish translation yet, the "es" column in the spreadsheet would be empty.

The purpose of this is to facilitate an audit of the translations, or to faciliate the translation process itself. After the spreadsheet has been audited/completed by a translator (such as in Excel), it can be re-imported into this repository - see below.

## Importing

@TODO: This hasn't been implemented yet.

An exported spreadsheet can be re-imported back into the repository, after having been edited, by running a Python script, and specifying a path to the file:

`python scripts/batch/import_translation_file /path/to/my-translation-file.csv`

Note that this only updates the .yml files, but it is still up to you to use Git to commit the changes and create a pull-request.