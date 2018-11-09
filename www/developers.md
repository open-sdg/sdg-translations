---
layout: page
title: Developers
permalink: developers/
---

## Repository

Development, discussion, and other forms of collaboration happen on the [Github repository]({{ site.repo }}).

## JSON output

The translations are compiled and available [here]({{ site.baseurl }}/translations.json).

## Previous releases

Each past release is available separately, according to its tag. For example, release 0.1.0 is available [here]({{ site.baseurl }}/translations-0.1.0.json).

## Importing spreadsheets from translators

As mentioned on the [translators page]({{ site.baseurl }}/translators), translators have access to automatically exported spreadsheets of translations. These spreadsheets can be re-imported back into the repository, after having been edited, by running a Python script, and specifying a path to the file:

`python scripts/import_translation_file /path/to/my-translation-file.csv`

Note that this only updates the .yml files, but it is still up to you to use Git to commit the changes and create a pull-request.

## Technical Limitations

* The language folders under `translations` (eg, `translations/en`, `translations/es`, etc.) cannot contain subfolders.
* The items in the .yml translation files can contain either strings or objects. However, in the case of objects, those objects can't contain other objects. For example, this will work:
    ```
    # Strings are fine
    hue: matiz
    # Objects containing strings are fine too
    colors:
      red: rojo
    ```

    But this will not work:
    ```
    # Objects containing objects - won't work.
    colors:
      red:
        light: luz rojo
        dark: rojo oscuro
    ```

## Local development

Requires Python and Ruby.

* `pipenv install`
* `bundle install`
* `make`

To serve the site locally:

* `make serve`

## Forking and builds

The origin repo is built by CirciCI and deployed to Github Pages. The configuration and scripts that accomplish this should work for forks as well, with a few steps.

[TODO: document steps for setting up CircleCI and Github Pages for forks]