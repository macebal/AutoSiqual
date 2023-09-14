env:
	source .env/Scripts/activate

install:
	python -m pip install -r requirements.txt

build:
	pyinstaller main.py --onefile --noconsole