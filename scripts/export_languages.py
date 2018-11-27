# -*- coding: utf-8 -*-
"""
Export all current languages into CSV files for easy translation.
"""

import export_translation_file as export

def main():

  current_languages = [
    'es',
    'fr',
    'zh-Hans',
    'ar',
    'ru',
  ]

  folder = 'www'

  for language in current_languages:
    export.export_language(language, folder)

  # Also, export a 'blank' one for new languages.
  export.export_language('blank', folder)

# Boilerplace syntax for running the main function.
if __name__ == '__main__':
  main()