## BASE IMAGE

# pulling official base image
FROM node:17.9-alpine AS base

# Setting working directory
WORKDIR /frontend
RUN chown -R node:node /frontend

COPY --chown=node:node package.json yarn.lock ./

USER node

# exposing ports
EXPOSE 3000

## DEV BUILD

FROM base as dev

# Cache and Install dependnecies
RUN yarn install

COPY --chown=node:node . .

# npm start
CMD [ "yarn", "start" ]

## PROD BUILD

FROM base as prod-build

RUN yarn install --prod \
    && yarn build

FROM nginx:stable-alpine as prod

COPY --from=prod-build /frontend/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
