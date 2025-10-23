venv:
	python -m venv venv
	venv\Scripts\activate && pip install -U pip && pip install -r requirements.txt

run:
	venv\Scripts\activate && python main.py

install:
	venv\Scripts\activate && pip install -r requirements.txt

clean:
	rmdir /s /q venv
	del /s /q __pycache__
	del /s /q *.pyc
