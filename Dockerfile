ARG IMAGE="python:3.9.1-slim-buster"

FROM $IMAGE as builder

ARG PY_PROJECT=remoteme

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.1.4

RUN apt-get -qq update \
    && apt-get install -qq -y --no-install-recommends libffi-dev libssl-dev libc6-dev gcc make openssh-client git curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN python3 -m venv /venv \
   && . /venv/bin/activate \
   && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/${POETRY_VERSION}/get-poetry.py > get-poetry.py \
   && python get-poetry.py -y --version ${POETRY_VERSION} \
   && rm get-poetry.py \
   && ${HOME}/.poetry/bin/poetry install --no-root;

COPY . /app/${PY_PROJECT}

RUN . /venv/bin/activate \
   && ${HOME}/.poetry/bin/poetry install;


FROM $IMAGE

ENV PYTHONUNBUFFERED 1
ENV PY_PROJECT=remoteme
ENV PATH="/venv/bin:${PATH}"

COPY --from=builder /app/${PY_PROJECT} /app
COPY --from=builder /venv /venv
COPY .ci /app/.ci

WORKDIR /app