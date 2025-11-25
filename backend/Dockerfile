FROM python:latest AS base
RUN python -m pip install temporalio

RUN groupadd -r app -g 1000 \
    && useradd -u 1000 -r -g app -m -d /home/app -s /bin/bash -c "App user" app

ENV APP_DIR /app
RUN mkdir -p $APP_DIR \
    && chown app:app $APP_DIR
COPY . $APP_DIR

### Development
FROM base AS dev

ENV APP_ENV dev
WORKDIR $APP_DIR
USER app

### Production
FROM base AS prod

ENV APP_ENV prod
WORKDIR $APP_DIR
USER app

