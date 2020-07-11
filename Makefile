none: help

help:
	@echo "DiamondQuest: A math mining adventure."
	@echo
	@echo "run			Run Word Peril."
	@echo "test			Run pytests for Word Peril."
	@echo "tidy			Tidy up cruft (pyc, pycache, eggs)."
	@echo
	@echo "venv			Build the venv based on requirements.txt & req-dev.txt"
	@echo "clean		Delete the venv"

clean:
	rm -r venv
.PHONY: clean

venv:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -r req-dev.txt

run: venv
	venv/bin/pip install .
	venv/bin/python3 -m wordperil
.PHONY: run

format: venv
	cd src && ../venv/bin/black -l 80 diamondquest
.PHONY: format

tidy: venv
	venv/bin/python3 -m pycleanup --egg --pyc --cache
.PHONY: tidy
