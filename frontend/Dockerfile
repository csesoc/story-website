# pulling official base image
FROM node:17.6-alpine

# Setting working directory
WORKDIR /frontend

# Cache and Install dependnecies
COPY --chown=node:node package.json .
RUN npm install 

COPY --chown=node:node . .
USER node

# exposing ports
EXPOSE 3000

# npm start
CMD [ "npm", "start" ]