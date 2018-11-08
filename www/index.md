---
layout: page
---
SDG Translations makes it easy to translate text related to the United Nation's
[Sustainable Development Goals](https://www.un.org/sustainabledevelopment/),
and to keep those translations available in one place, in both machine-friendly
and translator-friendly formats.

The machine-friendly translations are compiled and available [here]({{ site.baseurl }}translations.json).

## Translation search and context

A simple search app is available [here](https://opendataenterprise.github.io/sdg-translations) for finding the status of a particular translation. The results here may include contextual information as well, to help translators decide on the best translations.

Please let us know through the [issue queue](https://github.com/OpenDataEnterprise/sdg-translations/issues) if contextual information is needed about a particular translation.

## Previous releases

Each past release is available separately, according to its tag. For example, release 0.1.0 is available at:

https://opendataenterprise.github.io/sdg-translations/translations-0.1.0.json

## Exports for translation audits

The translations for the current languages are available in spreadsheet form for ease of translation audits. The spreadsheets avaiable include:
* [Spanish](https://opendataenterprise.github.io/sdg-translations/sdg-translations-es.csv)
* [French](https://opendataenterprise.github.io/sdg-translations/sdg-translations-fr.csv)
* [Chinese](https://opendataenterprise.github.io/sdg-translations/sdg-translations-zh.csv)

In these spreadsheets the English translations sit in a column alongside the translations for the target language, if any.

The purpose of this is to facilitate an audit of the translations, or to faciliate the translation process itself. After the spreadsheet has been audited/completed by a translator (such as in Excel), it can be re-imported into this repository - see below.

## New languages

Along the same lines as the exports mentioned above, there is a "blank" export available to help with new languages. That spreadsheet is available at:

https://opendataenterprise.github.io/sdg-translations/sdg-translations-blank.csv

## Manual exports

Exports can also be created by running a Python script, and specifying a 2-letter language code, like "es":

`python scripts/export_translation_file es`

## Importing

An exported spreadsheet can be re-imported back into the repository, after having been edited, by running a Python script, and specifying a path to the file:

`python scripts/import_translation_file /path/to/my-translation-file.csv`

Note that this only updates the .yml files, but it is still up to you to use Git to commit the changes and create a pull-request.
