# -*- coding: utf-8 -*-
import pandas as pd
import re
import unicodedata
import urllib
import os.path
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

def sdg_number_from_text(text):
  """
  This parses a string of text and pulls out the SDG number. Possible formats of
  return value are: '1', '1.1', '1.1.1'
  """
  if pd.isnull(text):
    return 'was null'

  matches = re.findall(r'(\d+)(\.\w+)?(\.\w+)?', text)
  if len(matches) > 0:
    return ''.join(matches[0])
  else:
    return 'no matches'

def sdg_text_without_number(text, number):
  """
  This simply removes a number from some text.
  """
  normalized = unicodedata.normalize("NFKD", str(text))
  return normalized.replace(number, '').strip()

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
  if not os.path.isfile(zip_filename):
    remote_url = 'https://unstats.un.org/sdgs/metadata/files/SDG-indicator-metadata.zip'
    urllib.request.urlretrieve(remote_url, zip_filename)
  with ZipFile(zip_filename, 'r') as zip:
    # printing all the contents of the zip file
    zip.printdir()

if __name__ == '__main__':
  main()