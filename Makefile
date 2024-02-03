# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.py"
# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.py"
# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\about.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\about.py"
export AUTOSIQUAL_HEADLESS_MODE=False

.PHONY: build

install:
	python -m pip install poetry==1.6.1
	poetry install

build:
	./bin/build.sh
	
run-dev:
	AUTOSIQUAL_HEADLESS_MODE=True poetry run python -m main

test:
	poetry run pytest

version-bump:
	./bin/version_bump.sh $(type)

open-gui-designer:
	./bin/open_qt_designer.sh

format:
	ruff format .

lint:
	ruff check . --fix