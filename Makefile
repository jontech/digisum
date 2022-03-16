all: test
.PHONY: test

test:
	venv/bin/pytest -s -v

devel:
	venv/bin/flask run
