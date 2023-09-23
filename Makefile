.PHONY: build

env:
	source .env/Scripts/activate

install:
	python -m pip install -r requirements.txt

build:
	pyinstaller main.py --onefile --noconsole
	cp config.json dist/config.json
	cp -fR img/ dist/

run-dev:
	python -m main