#
# SETTINGS
#
VIRTUALENV_FOLDER = venv


.PHONY: init lint test

init: ### Init development environment
	mkdir $(VIRTUALENV_FOLDER) || true
	python3 -m venv $(VIRTUALENV_FOLDER)
	source $(VIRTUALENV_FOLDER)/bin/activate && \
	pip install -r requirements.txt;
	gcloud auth application-default login

lint: ### Lint source files
	source $(VIRTUALENV_FOLDER)/bin/activate && \
	pylint src/

test: ### Run unit tests for project
	export FLASK_CONFIGURATION=test; \
	source $(VIRTUALENV_FOLDER)/bin/activate && \
	pytest --disable-pytest-warnings tests/
