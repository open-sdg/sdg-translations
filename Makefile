all: clean test build_data build_site

clean:
	rm -fr _site

test:
	pipenv run python scripts/check_translations.py

build_data:
	pipenv run python scripts/build_translations.py
	pipenv run python scripts/build_contexts.py
	pipenv run python scripts/export_languages.py

build_site:
	bundle exec jekyll build

serve:
	bundle exec jekyll serve --skip-initial-build
