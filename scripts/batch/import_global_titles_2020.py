# -*- coding: utf-8 -*-
import pandas as pd
import re
import unicodedata
import urllib
import os.path
import glob
import yaml

"""
This script imports the updated 2020 titles for goals, targets, and indicators.
In keeping with past imports, the id numbers (eg, 1.1.1, 1.1, etc) are stripped
from the beginnings of the titles.

Titles: Currently the titles are translated (at the UN level) into Arabic,
Chinese, Spanish, French, English, and Russian; however the Arabic
translations are only available as a PDF, which is more difficult to parse with
a script (and so are being skipped).
"""

def sdg_number_from_text(text):
  """
  This parses a string of text and pulls out the SDG number. Possible formats of
  return value are: '1', '1.1', '1.1.1'
  """
  if pd.isnull(text):
    return None

  matches = re.findall(r'(\d+)(\.\w+)?(\.\w+)?', text)
  if len(matches) > 0:
    match = ''.join(matches[0])
    # Sanity checks.
    match_parts = match.split('.')
    # In these cases, a missing space causes the first word
    # of the indicator title to appear as an extension of the
    # third id part.
    if len(match_parts) == 3 and len(match_parts[2]) > 2:
      match_2_replacement = ''
      for character in match_parts[2]:
        if character.isnumeric() or character.islower():
          match_2_replacement += character
        else:
          break
      if match_2_replacement != '' and match_2_replacement != match_parts[2]:
        match = match_parts[0] + '.' + match_parts[1] + '.' + match_2_replacement
    return match
  else:
    return None

def sdg_goal_is_valid(text):
  if text is None:
    return False
  parts = text.split('.')
  if len(parts) > 1:
    return False
  if not text.isnumeric():
    return False
  if int(text) > 17:
    return False
  return True

def sdg_indicator_is_valid(text):
  if text is None:
    return False
  parts = text.split('.')
  if len(parts) != 3:
    return False
  return True

def sdg_target_is_valid(text):
  if text is None:
    return False
  parts = text.split('.')
  if len(parts) != 2:
    return False
  return True

def sdg_text_without_number(text, number):
  """
  This simply removes a number from some text.
  """
  normalized = unicodedata.normalize("NFKD", str(text))
  # Remove the number and everything before it.
  parts = normalized.split(number)
  if len(parts) == 2:
    return parts[1].lstrip('.').strip()
  else:
    return normalized

def clean_indicator_title(title):
  last = title[-1]
  if last == 'i':
    return title[:-1]
  if last.isnumeric():
    last_word = title.split(' ')[-1]
    last_word = last_word.split('-')[-1]
    last_word = last_word.split('–')[-1]
    last_word = last_word.split('‐')[-1]
    last_word = last_word.split('+B')[-1]
    if not last_word.isnumeric():
      print('Found a footnote: ' + title)
      return title[:-1]
  return title

def clean_target_title(title):
  last = title[-1]
  if last.isnumeric() and last != '0':
    return title[:-1]
  return title

def clean_goal_title(title):
  last = title[-1]
  if last.isnumeric():
    return title[:-1]
  return title

def main():
  global_goals = {}
  global_targets = {}
  global_indicators = {}

  # First, the titles.
  title_spreadsheets = {
    'en': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%202020%20review_English.xlsx',
    'zh-Hans': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%202020%20review_Chinese.xlsx',
    'es': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%202020%20review_Spanish.xlsx',
    'fr': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%202020%20review_French.xlsx',
    'ru': 'https://unstats.un.org/sdgs/indicators/Global%20Indicator%20Framework%20after%202020%20review_Russian.xlsx'
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
      #'encoding': 'utf-8',
    }

    df = pd.read_excel(spreadsheet_url, **import_options)
    for _, row in df.iterrows():
      # If the 'indicator' column in empty, this is a Goal.
      if pd.isnull(row['indicator']):
        # Identify the goal number.
        goal_number = sdg_number_from_text(row['target'])
        goal_is_valid = sdg_goal_is_valid(goal_number)
        if goal_is_valid and goal_number and goal_number + '-title' not in global_goals[language]:
          goal_text = sdg_text_without_number(row['target'], goal_number)
          global_goals[language][goal_number + '-title'] = clean_goal_title(goal_text)
      else:
        # Otherwise it is a target and indicator.
        target_number_dots = sdg_number_from_text(row['target'])
        target_number = None if target_number_dots is None else target_number_dots.replace('.', '-')
        if target_number and sdg_target_is_valid(target_number_dots) and target_number + '-title' not in global_targets[language]:
          target_text = sdg_text_without_number(row['target'], target_number_dots)
          global_targets[language][target_number + '-title'] = clean_target_title(target_text)
        indicator_number_dots = sdg_number_from_text(row['indicator'])
        indicator_number = None if indicator_number_dots is None else indicator_number_dots.replace('.', '-')
        if indicator_number and sdg_indicator_is_valid(indicator_number_dots) and indicator_number + '-title' not in global_indicators[language]:
          indicator_text = sdg_text_without_number(row['indicator'], indicator_number_dots)
          global_indicators[language][indicator_number + '-title'] = clean_indicator_title(indicator_text)

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
        yaml_data = yaml.load(stream, Loader=yaml.FullLoader)
      if not yaml_data:
        yaml_data = {}
      for item in all_results[yaml_filename][language]:
        yaml_data[item] = all_results[yaml_filename][language][item]
      with open(translation_path, 'w') as outfile:
        yaml.dump(yaml_data, outfile, default_flow_style=False, allow_unicode=True)

if __name__ == '__main__':
  main()