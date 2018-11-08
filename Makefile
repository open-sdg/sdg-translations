all: clean build

clean:
		rm -fr _site

build:
		bundle exec jekyll build
		python3 scripts/build_translations.py
		python3 scripts/build_contexts.py
		python3 scripts/export_languages.py

serve:
		bundle exec jekyll serve --skip-initial-build
