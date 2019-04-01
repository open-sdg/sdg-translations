"""
Use Google to translate a Yaml file of English strings.
"""

import sys
import yaml
from google.cloud import translate

if len(sys.argv) < 3:
  sys.exit('Provide an input file and a 2-letter abbreviation for the target language.')

input_file = sys.argv[1]
language = sys.argv[2]

translate_client = translate.Client()
with open(input_file, 'r') as stream:
  yamldata = yaml.load(stream)

for key in yamldata:
  translation = translate_client.translate(yamldata[key], target_language=language)
  yamldata[key] = translation['translatedText']

with open('output.yml', 'w') as outfile:
  yaml.dump(yamldata, outfile, default_flow_style=False, sort_keys=False, allow_unicode=True)
