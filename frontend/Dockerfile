FROM node:latest AS base

#RUN groupadd -r app -g 1000\
#    && useradd -u 1000-r -g app -m -d /home/app -s /bin/bash -c "App user" app

ENV APP_DIR /app
RUN mkdir -p $APP_DIR \
    && chown node:node $APP_DIR
COPY . $APP_DIR

### Development
FROM base AS dev

ENV APP_ENV dev
WORKDIR $APP_DIR
USER node

### Production
FROM base AS prod

ENV APP_ENV prod
WORKDIR $APP_DIR
USER node

