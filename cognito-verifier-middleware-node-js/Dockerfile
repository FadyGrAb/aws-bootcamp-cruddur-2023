FROM node:16-alpine

WORKDIR /cognito-verifier-middleware

COPY index.js package-lock.json package.json server.cjs /cognito-middleware/

RUN npm install

CMD [ "node", "index.js" ]