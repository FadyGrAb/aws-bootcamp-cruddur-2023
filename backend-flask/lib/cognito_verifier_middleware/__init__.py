import os
import json

import requests
from .exceptions import *
from flask import Flask, request


class CognitoVerifierMiddleware:
    def __init__(self, app: Flask) -> None:
        self.app = app
        endpoint = os.getenv("COGNITO_VERIFIER_URL", None)
        if endpoint:
            self._endpoint = endpoint
        else:
            # pass
            raise EndpointNotSetException

        # Test connection
        self._test_conntection()

    @property
    def token_is_valid(self):
        try:
            token = self._extract_token()
        except TokenNotFoundException:
            return False

        cognito_verifier_response = requests.get(
            f"{self._endpoint}/verify?token={token}"
        )

        if cognito_verifier_response.status_code == 200:
            self._token_payload = json.loads(cognito_verifier_response.content)

        return cognito_verifier_response.status_code == 200

    @property
    def cognito_user_id(self):
        # return self._token_payload.get("username", "something went wrong")
        return self._token_payload.get("sub", "something went wrong")

    def _extract_token(self):
        auth_header = request.headers.get("Authorization")
        if auth_header and (" " in auth_header):
            _, access_token = auth_header.split()
        else:
            raise TokenNotFoundException(auth_header)

        return access_token

    def _test_conntection(self):
        test_connection = requests.get(self._endpoint)

        if test_connection.status_code != 200:
            raise EndpointConnectionFailedException(test_connection, self._endpoint)
        else:
            self.app.logger.info("Cognito Verifier middleware connection test passed.")

    def jwt_required(self, func, run_without_jwt=None):
        try:
            if self.token_is_valid:
                func()
            elif run_without_jwt:
                run_without_jwt()
            else:
                return {}, 403
        except TokenNotFoundException as e:
            print(e)
            return {}, 401
