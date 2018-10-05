# -*- coding: utf-8 -*-
import pandas as pd
import re
import unicodedata
import urllib
import os.path
import PyPDF2
import glob
import yaml
import shutil
from zipfile import ZipFile

"""
This script tries to get as much official United Nations metadata as possible
about the SDG goals, targets, and indicators.

Titles: Currently the titles are translated (at the UN level) into Arabic,
Chinese, Spanish, French, English, and Russian; however the Arabic and Russian
translations are only available as a PDF, which is more difficult to parse with
a script (and so are being skipped).

Other metadata: The other global metadata is only available in English, so this
script only grabs the UN metadata for English.
"""

def find_between(s, start, end):
  if start not in s or end not in s:
    return None
  between = (s.split(start))[1].split(end)[0]
  return between.strip()

def sdg_number_from_text(text):
  """
  This parses a string of text and pulls out the SDG number. Possible formats of
  return value are: '1', '1.1', '1.1.1'
  """
  if pd.isnull(text):
    return None

  matches = re.findall(r'(\d+)(\.\w+)?(\.\w+)?', text)
  if len(matches) > 0:
    return ''.join(matches[0])
  else:
    return None

def sdg_text_without_number(text, number):
  """
  This simply removes a number from some text.
  """
  normalized = unicodedata.normalize("NFKD", str(text))
  # Remove numerals from the end, to deal with footnotes.
  for footnote in range(1, 9):
    normalized = normalized.rstrip(str(footnote))
  # Remove the number and everything before it.
  parts = normalized.split(number)
  if len(parts) == 2:
    return parts[1].lstrip('.').strip()
  else:
    return normalized

def main():
  global_goals = {}
  global_targets = {}
  global_indicators = {}

  # First, the titles.
  title_spreadsheets = {
    'en': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%20refinement.English.xlsx',
    'zh': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%20refinement.Chinese.xlsx',
    'es': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%20refinement.Spanish.xlsx',
    'fr': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%20refinement.French.xlsx',
  }
  for language in title_spreadsheets:

    global_goals[language] = {}
    global_targets[language] = {}
    global_indicators[language] = {}

    spreadsheet_url = title_spreadsheets[language]
    import_options = {
      'header': None,
      'names': ['target', 'indicator'],
      'usecols': [1, 2],
      'skiprows': [0, 1, 2],
      'skipfooter': 6,
      'encoding': 'utf-8',
    }

    df = pd.read_excel(spreadsheet_url, **import_options)
    for index, row in df.iterrows():
      # If the 'indicator' column in empty, this is a Goal.
      if pd.isnull(row['indicator']):
        # Identify the goal number.
        goal_number = sdg_number_from_text(row['target'])
        if goal_number and goal_number not in global_goals[language]:
          goal_text = sdg_text_without_number(row['target'], goal_number)
          global_goals[language][goal_number] = {'title': goal_text}
      else:
        # Otherwise it is a target and indicator.
        #print(row)
        target_number = sdg_number_from_text(row['target'])
        if target_number and target_number not in global_targets[language]:
          target_text = sdg_text_without_number(row['target'], target_number)
          global_targets[language][target_number] = {'title': target_text}
        indicator_number = sdg_number_from_text(row['indicator'])
        if indicator_number and indicator_number not in global_indicators[language]:
          indicator_text = sdg_text_without_number(row['indicator'], indicator_number)
          global_indicators[language][indicator_number] = {'title': indicator_text}

  # Next get the (Engish only, currently) metadata.
  zip_filename = 'SDG-indicator-metadata.zip'
  unzip_folder = 'temp-import-files'
  remote_url = 'https://unstats.un.org/sdgs/metadata/files/SDG-indicator-metadata.zip'
  urllib.request.urlretrieve(remote_url, zip_filename)
  with ZipFile(zip_filename, 'r') as zip:
    zip.extractall(unzip_folder)

  for filepath in glob.iglob(unzip_folder + '/*.pdf'):
    # Figure out the indicator number.
    indicator = filepath.replace(unzip_folder, '')
    indicator = indicator.replace(os.sep + 'Metadata-', '')
    indicator = indicator.replace('.pdf', '')
    indicator_parts = indicator.split('-')
    indicator = '.'.join(map(lambda x: x.lstrip('0').lower(), indicator_parts))

    if indicator not in global_indicators['en']:
      global_indicators['en'][indicator] = {}

    pdfFileObject = open(filepath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.getNumPages()
    pdfContent = ''
    for i in range(count):
      page = pdfReader.getPage(i)
      pdfContent += page.extractText()

    # Next we use a series of very fragile tricks for getting certain metadata.
    # Mostly we look for text on either side of what we're looking for.
    organization = find_between(pdfContent, 'Organization(s):', 'Concepts and definitions')
    if organization:
      organizations = organization.split('\n \n')
      organizations = list(map(lambda x: x.replace('\n', ''), organizations))
      organization = ', '.join(organizations)
      organization = organization.strip()
    if organization and organization != '':
      global_indicators['en'][indicator]['custodian_agency'] = organization

    description = find_between(pdfContent, 'Definition:', 'Rationale:')
    if description:
      description = description.replace('\n', '').strip()
    if description and description != '':
      global_indicators['en'][indicator]['definition'] = description

    # Just guess at the remote link from the filepath.
    remote_folder = 'https://unstats.un.org/sdgs/metadata/files/'
    remote_link = filepath.replace(unzip_folder + os.sep, remote_folder)
    global_indicators['en'][indicator]['metadata_link'] = remote_link

  # Finally merge the results into the YAML files.
  all_results = {
    'global_goals.yml': global_goals,
    'global_targets.yml': global_targets,
    'global_indicators.yml': global_indicators,
  }
  for yaml_filename in all_results:
    for language in all_results[yaml_filename]:
      translation_path = os.path.join('translations', language, yaml_filename)
      yaml_data = None
      with open(translation_path, 'r') as stream:
        yaml_data = yaml.load(stream)
      if not yaml_data:
        yaml_data = {}
      for item in all_results[yaml_filename][language]:
        if item not in yaml_data:
          yaml_data[item] = all_results[yaml_filename][language][item]
        else:
          for key in all_results[yaml_filename][language][item]:
            yaml_data[item][key] = all_results[yaml_filename][language][item][key]
      with open(translation_path, 'w') as outfile:
        yaml.dump(yaml_data, outfile, default_flow_style=False, allow_unicode=True)

  # Clean up.
  shutil.rmtree(unzip_folder)
  os.remove(zip_filename)

if __name__ == '__main__':
  main()