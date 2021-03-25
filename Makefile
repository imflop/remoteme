PYTHON_BIN := python3
VENV_NAME := .venv
PIP_VERSION := 21.0.1
POETRY_VERSION := 1.1.4
PIP_VERSION := 20.2.4
MAX_LINE_LENGTH := 120
POETRY_BIN := ${HOME}/.poetry/bin/poetry

.PHONY: help poetry prepare

help:
	@echo "HELP"
	@echo ""
	@echo "  poetry - install poetry"
	@echo "  prepare - make venv and deps"

poetry:
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/${POETRY_VERSION}/get-poetry.py > get-poetry.py \
	&& ${PYTHON_BIN} get-poetry.py --version ${POETRY_VERSION} -y \
	&& rm get-poetry.py

prepare:
	${PYTHON_BIN} -m venv ${VENV_NAME} \
	&& . ${VENV_NAME}/bin/activate \
	&& ${POETRY_BIN} run pip install pip==${PIP_VERSION} \
	&& ${POETRY_BIN} install;

format:
	python -m black . -l ${MAX_LINE_LENGTH}

lint:
	python -m isort .

clean:
	[ -n "${VENV_NAME}" ] && rm -rf ./${VENV_NAME}
	find . -name "*.pyc" -delete