ARG ECR_NODEJS_URL
FROM ${ECR_NODEJS_URL}:16-alpine

WORKDIR /cognito-verifier-middleware

COPY index.js package-lock.json package.json server.cjs /cognito-verifier-middleware/

RUN npm install

CMD [ "node", "index.js" ]