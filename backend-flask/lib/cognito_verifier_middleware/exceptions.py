class EndpointNotSetException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "The endpoint env variable 'COGNITO_VERIFIER_URL' is not set"


class EndpointConnectionFailedException(Exception):
    def __init__(self, response_content, endpoint, *args: object) -> None:
        super().__init__(*args)
        self.response_content = response_content
        self.endpoint = endpoint

    def __str__(self) -> str:
        return f"Something went wrong when contacting the Cognito Vefifier {self.endpoint}: {self.response_content}"


class TokenNotFoundException(Exception):
    def __init__(self, auth_header, *args: object) -> None:
        super().__init__(*args)
        self.auth_header = auth_header

    def __str__(self) -> str:
        return f"Unable to find a token in the correct format. Received the following auth header {self.auth_header}"
