"use strict";
const { CognitoJwtVerifier } = require("aws-jwt-verify");
//const { assertStringEquals } = require("aws-jwt-verify/assert");

const jwtVerifier = CognitoJwtVerifier.create({
  userPoolId: process.env.USER_POOL_ID,
  tokenUse: "access",
  clientId: process.env.CLIENT_ID, //,
  //customJwtCheck: ({ payload }) => {
  //  assertStringEquals("e-mail", payload["email"], process.env.USER_EMAIL);
  //},
});

exports.handler = async (event) => {
  console.log("request:", JSON.stringify(event, undefined, 2));

  const jwt = event.headers.authorization.split(" ")[1];
  let isAuthorized = false;
  try {
    const payload = await jwtVerifier.verify(jwt);
    console.log("Access allowed. JWT payload:", payload);
    isAuthorized = true
  } catch (err) {
    console.error("Access forbidden:", err);
  
  } finally {
    const response = {
      "isAuthorized": isAuthorized,
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",
        "Access-Control-Allow-Origin": "https://3000-fadygrab-awsbootcampcru-vig6yhzhbn6.ws-eu94.gitpod.io",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
      }
    };
    console.log(response)
    return response
  }
  
};