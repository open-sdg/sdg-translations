---
layout: page
title: Change Log
permalink: changelog/
---

Numbers in parenthesis below refer to Github issues or pull-requests.

## 0.4.0

## Breaking changes

* Include token for country name in translations of frontpage.header (#56)

### Functionality

* Move this changelog to the site (#52)
* Add goal images to this project for all languages (#58)

### Translations

* Fix placement of tokens in frontpage.instructions (#34, #53)
* Add translations of "target" and "targets" (#35, #54)
* Add Armenian translations (#37, #38, #39, #42)
* Fix error in English version of 5.3.1 (#41)
* Sentence casing for some short goal titles in English (#46, #51)
* Add/fix German translations (#47, #59, #61, #65)

## 0.3.2

### Functionality

* Switch to using the master branch, for simplicity (#28)
* Trigger builds on tagging (#29)

### Translations

* Arabic fixes. (#24)
* Spanish fixes. (#25, #26, #27)

## 0.3.0

### Breaking changes

* Change Chinese code from "zh" to "zh-Hans" (d217b4b6)

### Functionality

* Omit certain keys from translation CSV exports. (#13)
* Search page for looking for contextual information (#16)
* Revamp the repository to use Jekyll for the www pages. (#19)
* Allow imports when folder does not exist (7e0bcc9a)
* Bug fix: import script preserves existing data (3968aa20)

### Translations

* Added context about some translations (#17)
* Added Arabic translations (#20)
* Added Russian translations (#21)
* Change Chinese code from "zh" to "zh-Hans" (d217b4b6)
* Added Simplified Chinese translations (16b18d4d)

## 0.2.0

### Translations

* Ran a script to import official Spanish, French, and Chinese translations from UN sources. This changed some existing Spanish and French translations (slightly) and added new Chinese translations. (#6)

### Functionality

* Export/import functionality so translators can work with CSV files (#4 and #5)
* Automatically export CSV translation files during build process (#8)
* Script for importing metadata from UN sources (#6)

## 0.1.0

This is the initial release, starting with translations for Spanish and French. The indicator and goal titles were pulled in from the [GSA/sdg-indicators](https://github.com/GSA/sdg-indicators) repository. All others through Google Translate.