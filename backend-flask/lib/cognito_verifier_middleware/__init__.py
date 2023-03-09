import logging
import os

import requests
from exceptions import *
from flask import Flask, request

logger = logging.getLogger("Cognito Verifier")
logger.setLevel(logging.DEBUG)


class CognitoVerifierMiddleware:
    def __init__(self, app: Flask) -> None:
        endpoint = os.getenv("COGNITO_VERIFIER_URL", None)
        if endpoint:
            self._endpoint = endpoint
        else:
            raise EndpointNotSetException

        # Test connection
        self._test_conntection()

        self.app = app

    @property
    def token_is_valid(self):
        token = self._extract_token()
        cognito_verifier_response = requests.get(
            f"{self._endpoint}/verify?token={token}")
        return cognito_verifier_response.status_code == 200

    @property
    def username(self):
        pass

    def _extract_token(self):
        auth_header = request.headers.get("Authorization")
        if auth_header and (" " in auth_header):
            _, access_token = auth_header.split()
        else:
            raise TokenNotFoundException

        return access_token

    def _test_conntection(self):
        test_connection = requests.get(self._endpoint)

        if test_connection.status_code != 200:
            raise EndpointConnectionFailedException(test_connection)
        else:
            logger.info("Cognito Verifier middleware connection test passed.")
