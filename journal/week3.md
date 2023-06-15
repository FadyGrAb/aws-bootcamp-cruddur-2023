# Week 3 — Decentralized Authentication

## Table of Contents

- [Required Homework](#required-homework)
  - [Setup Cognito User Pool](#setup-cognito-user-pool)
  - [Implement Custom Signin Page](#implement-custom-signin-page)
  - [Implement Custom Signup Page](#implement-custom-signup-page)
  - [Implement Custom Confirmation Page](#implement-custom-confirmation-page)
  - [Implement Custom Recovery Page](#implement-custom-recovery-page)
- [Homework Challenges](#homework-challenges)
  - [Using a decoupled _Cognito-verifier_ middleware that uses "_aws-cognito-verify.js_"](#using-a-decoupled-cognito-verifier-middleware-that-uses-aws-cognito-verifyjs)

## Required Homework:

### Setup Cognito User Pool:

I've create a cognito user pool as per the video instructions adding the "preferred_username" attribute as required.  
![cognito user pool](assests/week03/hwreq-0101-cognito-user-pool.png)  
![preferred_username](assests/week03/hwreq-0102-cognito-user-pool.png)

### Implement Custom Signin Page:

I've created the signin page and singed in with a previously created user "fady"  
![logged in user](assests/week03/hwreq-0201-singin.png)  
![singing in demo](assests/week03/hwreq-0202-singin.gif)  
I've noticed that the backend throws errors due to missing _jose_ module when I started a new workspace after I had implemented the page following the video class earlier. I just added _python-jose_ to the _requirements.txt_ file and this solved the problem.

### Implement Custom Signup Page:

I've created the signup page and used it to create another user (fady2) and confirmed it in Congito UI in the AWS console.  
![singing up demo](assests/week03/hwreq-0301-singup.gif)  
![new user in cognito](assests/week03/hwreq-0302-singup.png)

### Implement Custom Confirmation Page:

The confirmation page is also implemented (is shown in the **_Implement Custom Signup Page_** demo). I received the verification OTP via email and the new user (fady2)'s email has the "verified" status.  
![confirmation](assests/week03/hwreq-0401-confirmation.gif)  
![verification email](assests/week03/hwreq-0402-confirmation.png)
![verified status](assests/week03/hwreq-0403-confirmation.png)

### Implement Custom Recovery Page:

I've implemented the Recovery Page. And to demonstrate that it is working, I've reset the password of the (fady2) user and logged in with the new password.  
![recovery demo](assests/week03/hwreq-0501-recovery.gif)  
![recovery mail](assests/week03/hwreq-0502-recovery.png)

## Homework Challenges:

### Using a decoupled _Cognito-verifier_ middleware that uses "_aws-cognito-verify.js_":

I've successfully decoupled the verification from the app using a containerized Node.js server that uses _"aws-jwt-verify.js"_. This is my first time writing JS code (I come from Python background) and a Node.js app. While writing the Node.js server, I did a lot of searching and trial and errors. One roadblock I've encountered is that I've discovered that JS has two types of modules, The ES and common. And you can't _directly_ use both in the same file.  
I've overcome this hurdle again by doing lots of searching and a bit of experimentation on my end. The reason I need to use both ES and Common modules is that I use _express.js_ (a web framework) which is a Common module and _aws-jwt-verify.js_ which is an ES module. The following steps solved the issue:

- Separate the common module in its own file with _.cjs_ extension and export the object(s) you need to use in with the ES module.

```javascript
//server.cjs
let express = require("express");
let app = express();

module.exports = app;
```

- Import the "common objects" normally in the ES module.

```javascript
//index.js
...
import app from "./server.cjs";
...
```

- Change the _type_ in _package.json_ to _module_.

For the decoupling to work, I've written:

1. The Node.js server and containerized it as **_cognito-verifier_** service in the _docker-compose.yaml_ file and published port 5555 for the container as this is the port that the verifier listens to. Its API has two endpoints:
   1. "_/_": The home endpoints and I use it as healthcheck endpoint (the python class use it to test the connectivity).
   2. "_/verify?token=\<token\>_": The main endpoint where the verification happens. In case of successful verification, the server returns a **_200_** status code and the content (claim) retrieved from the token otherwise, it returns **_422_**.
2. The python package **_cognito_verifier_middleware_** which contains the **_CognitoVerifierMiddleware_** class that handles the communications with the middleware (containerized Node.js server).

In order to use the Python class, all I need to do is import it from the **_cognito_verifier_middleware_** package and instantiate it:

```python
# app.py
...
from lib.cognito_verifier_middleware import CognitoVerifierMiddleware
...
cognito_verifier = CognitoVerifierMiddleware(app)
...
```

To verify the JWT token, just test for its **_token_is_valid_** property which returns a boolean value (True if the token is valid)

```python
if cognito_verifier.token_is_valid:
        # Do something if the token is valid
    else:
        # Do something if the token is invalid
```

To get the _username_ from the token (cognito_user_id), just use the class's **_cognito_user_id_** property provided that the token is verified.

```python
cognito_user_id = cognito_verifier.cognito_user_id
```

The class abstracts all the communications with the middleware and payload (claim) processing.

I didn't write a testing script for the class nor handled the errors properly as my goal was just to get it working similar to the original implementation in the video class and it did. In fact all the demos in the **_Required Homework_** section are using my middleware implementation and it returned the same cognito user ID as in the AWS console.  
![cognito user ID](assests/week03/hwch-0101-verify.gif)  
![user ID AWS console](assests/week03/hwch-0102-verify.png)
