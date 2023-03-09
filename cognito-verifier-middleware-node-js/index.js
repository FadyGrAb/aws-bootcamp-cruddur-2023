import { CognitoJwtVerifier } from "aws-jwt-verify";
import app from "./server.cjs";

// let app = require("express");

const verifier = CognitoJwtVerifier.create({
  userPoolId: process.env.AWS_COGNITO_USER_POOL_ID,
  tokenUse: "access",
  clientId: process.env.AWS_COGNITO_USER_POOL_CLIENT_ID,
});

app.get("/verify", async function (request, response) {
  let token = request.query.token;
  try {
    const payload = await verifier.verify(
      token // the JWT as string
    );
    console.log("Token is valid. Payload:", payload);
    response.status(200).send("token is valid");
  } catch {
    console.log("Token not valid!");
    response.status(422).send("token is invalid");
  }
});

app.get("/", function (request, response) {
  response.status(200).json({ message: "Cognito verifier middleware is up!" });
});

app.listen(5555, function () {
  let currentDateTime = new Date();
  console.log(`[${currentDateTime}] Server is running on port 5555`);
});
