all: clean test build

dependencies:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r scripts/requirements.txt
	bundle install

clean:
	rm -fr _site

test:
    . venv/bin/activate
    python3 scripts/check_translations.py

build:
    . venv/bin/activate
	python3 scripts/build_translations.py
	python3 scripts/build_contexts.py
	python3 scripts/export_languages.py
	bundle exec jekyll build

serve:
	bundle exec jekyll serve --skip-initial-build
