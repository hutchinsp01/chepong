FROM python:3.11-slim as os-base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update
RUN apt-get install -y curl

FROM os-base as poetry-base

RUN curl -sSL https://install.python-poetry.org/ | python -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false
RUN apt-get remove -y curl
RUN rm -rf /var/lib/apt/lists/* \
RUN rm -rf /var/cache/apt/

FROM poetry-base as app-base

ARG APPDIR=/app
WORKDIR $APPDIR/

COPY app ./app
COPY pyproject.toml poetry.lock /app/
COPY manage.py ./manage.py

RUN poetry install --no-dev && rm -rf /root/.cache/pypoetry

FROM app-base as main