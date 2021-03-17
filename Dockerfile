ARG IMAGE="python:3.9.1-slim-buster"

FROM $IMAGE

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.1.4

RUN apt-get -qq update \
    && apt-get install -qq -y --no-install-recommends libffi-dev libssl-dev libc6-dev gcc make openssh-client git curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN python3 -m venv /app/venv \
   && . /app/venv/bin/activate \
   && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/${POETRY_VERSION}/get-poetry.py > get-poetry.py \
   && python get-poetry.py -y --version ${POETRY_VERSION} \
   && rm get-poetry.py \
   && ${HOME}/.poetry/bin/poetry install --no-root;

COPY . /app/

RUN . /app/venv/bin/activate \
   && ${HOME}/.poetry/bin/poetry install;