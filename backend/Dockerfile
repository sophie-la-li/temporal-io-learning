
FROM python:latest AS base

RUN groupadd -r app -g 1000 \
    && useradd -u 1000 -r -g app -m -d /home/app -s /bin/bash -c "App user" app

ENV APP_DIR /app
RUN mkdir -p $APP_DIR \
    && chown app:app $APP_DIR
COPY . $APP_DIR

WORKDIR $APP_DIR
USER app

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:/home/app/.local/bin"
