all: test
.PHONY: test

test:
	venv/bin/pytest -s -v
