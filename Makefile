all: clean test build_data build_site

clean:
	rm -fr _site

test:
	python scripts/check_translations.py

build_data:
	python scripts/build_translations.py
	python scripts/build_contexts.py
	python scripts/export_languages.py

build_site:
	bundle exec jekyll build

serve:
	bundle exec jekyll serve --skip-initial-build
