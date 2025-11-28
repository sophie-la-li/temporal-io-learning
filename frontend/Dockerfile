
FROM node:latest AS base

ENV APP_DIR /app
RUN mkdir -p $APP_DIR \
    && chown node:node $APP_DIR
COPY . $APP_DIR

WORKDIR $APP_DIR
USER node
