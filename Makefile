# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.py"
# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.py"
# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\about.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\about.py"

.PHONY: build

install:
	python -m pip install poetry==1.6.1
	poetry install

build:
	./bin/build.sh
	
run-dev:
	python -m main

version-bump:
	./bin/version_bump.sh $(version_bump_type)

open-gui-designer:
	./bin/open_qt_designer.sh