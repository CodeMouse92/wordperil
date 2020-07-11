clean:
	rm -r venv
.PHONY: clean

venv:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

run: venv
	venv/bin/pip install .
	venv/bin/python3 -m wordperil

.PHONY: run
