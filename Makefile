# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\gui.py"
# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\log.py"
# pyuic5 "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\about.ui" -o "C:\\Users\\macebal\\Desktop\\Python\\GUI\\AutoSiqual v2\\about.py"

.PHONY: build

install:
	python -m pip install poetry==1.6.1
	poetry install

build:
	pyinstaller main.py --onefile --noconsole
	cp config.json dist/config.json
	cp -fR img/ dist/

run-dev:
	python -m main