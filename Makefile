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