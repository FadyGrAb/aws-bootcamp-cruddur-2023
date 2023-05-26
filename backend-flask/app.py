from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os
import uuid
import random

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.users_short import *
from services.update_profile import *

# Honeycomb imports
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# AWS X-Ray imports
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# CloudWatch logs imports
import watchtower
import logging
from time import strftime

# Rollbar imports
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

from lib.cognito_jwt_token import CognitoJwtToken, TokenVerifyError, TokenExpiredError
from flask import abort, make_response, jsonify

# My cognito middlware implimentation
from lib.cognito_verifier_middleware import CognitoVerifierMiddleware
from lib.cognito_verifier_middleware.exceptions import *

app = Flask(__name__)


# Initialize Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Initialize X-ray
# xray_url = os.getenv("AWS_XRAY_URL")
# xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# XRayMiddleware(app, xray_recorder)

# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler("cruddur")
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("test-log")

# Init Rollbar
rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")

# Init my cognito middleware
cognito_verifier = CognitoVerifierMiddleware(app)


frontend = os.getenv("FRONTEND_URL")
backend = os.getenv("BACKEND_URL")
origins = [frontend, backend]
cors = CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    headers=["Content-Type", "Authorization"],
    expose_headers="Authorization",
    methods="OPTIONS,GET,HEAD,POST",
)

cognito_jwt_token = CognitoJwtToken(
    user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"),
    user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
    region=os.getenv("AWS_DEFAULT_REGION"),
)


@app.route("/api/health-check")
def health_check():
    return {"success": True, "ver": 2}, 200


@app.route("/api/message_groups", methods=["GET"])
def data_message_groups():
    try:
        if cognito_verifier.token_is_valid:
            model = MessageGroups.run(cognito_user_id=cognito_verifier.cognito_user_id)
            # print("=====> data_message_groups", model)
            # user_handle = 'andrewbrown'
            if model["errors"] is not None:
                return model["errors"], 422
            else:
                return model["data"], 200
        else:
            # print("=====> data_message_groups, token_is_valid", cognito_verifier.token_is_valid)
            return {}, 401
    except TokenNotFoundException as e:
        print(e)
        return {}, 401


@app.route("/api/messages/<string:message_group_uuid>", methods=["GET"])
def data_messages(message_group_uuid):
    try:
        if cognito_verifier.token_is_valid:
            # print(">>>>>>>>>>> app.py, messages, message_group_uuid", message_group_uuid)
            model = Messages.run(
                message_group_uuid=message_group_uuid,
                cognito_user_id=cognito_verifier.cognito_user_id,
            )
            if model["errors"] is not None:
                return model["errors"], 422
            else:
                return model["data"], 200
        else:
            return {}, 401
    except TokenNotFoundException as e:
        print(e)
        return {}, 401


@app.route("/api/messages", methods=["POST", "OPTIONS"])
@cross_origin()
def data_create_message():
    user_receiver_handle = request.json.get("handle", None)
    message_group_uuid = request.json.get("message_group_uuid", None)
    message = request.json["message"]
    try:
        if cognito_verifier.token_is_valid:
            if message_group_uuid == None:
                # Create for the first time
                model = CreateMessage.run(
                    mode="create",
                    message=message,
                    cognito_user_id=cognito_verifier.cognito_user_id,
                    user_receiver_handle=user_receiver_handle,
                )
            else:
                # Push onto existing Message Group
                model = CreateMessage.run(
                    mode="update",
                    message=message,
                    message_group_uuid=message_group_uuid,
                    cognito_user_id=cognito_verifier.cognito_user_id,
                )
            if model["errors"] is not None:
                return model["errors"], 422
            else:
                return model["data"], 200
        else:
            return {}, 401
    except TokenNotFoundException as e:
        print(e)
        return {}, 401


@app.route("/api/activities/home", methods=["GET"])
def data_home():
    ### Video Class implementation ###
    # access_token = CognitoJwtToken.extract_access_token(request.headers)
    # try:
    #     cognito_jwt_token.verify(access_token)
    #     claims = cognito_jwt_token.claims
    #     cognito_user_id = claims.get("username", "something went wrong")
    #     data = HomeActivities.run(
    #         cognito_user_id=cognito_user_id, logger=LOGGER)
    # except TokenVerifyError as e:
    #     data = HomeActivities.run(logger=LOGGER)
    # except TokenExpiredError as e:
    #     data = HomeActivities.run(logger=LOGGER)

    # My cognito middleware implimentation
    if cognito_verifier.token_is_valid:
        cognito_user_id = cognito_verifier.cognito_user_id
        data = HomeActivities.run(cognito_user_id=cognito_user_id, logger=LOGGER)
    else:
        data = HomeActivities.run(logger=LOGGER)
    return data, 200


@app.route("/api/activities/notifications", methods=["GET"])
def data_notifications():
    data = NotifictionsActivities.run()
    return data, 200


@app.route("/api/activities/@<string:handle>", methods=["GET"])
def data_handle(handle):
    model = UserActivities.run(handle)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/activities/search", methods=["GET"])
def data_search():
    term = request.args.get("term")
    model = SearchActivities.run(term)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities():
    # user_handle = 'andrewbrown'
    # user_handle = request.json["user_handle"]
    message = request.json["message"]
    ttl = request.json["ttl"]
    try:
        if cognito_verifier.token_is_valid:
            model = CreateActivity.run(message, cognito_verifier.cognito_user_id, ttl)
            if model["errors"] is not None:
                return model["errors"], 422
            else:
                return model["data"], 200
        else:
            return {}, 401
    except TokenNotFoundException as e:
        print(e)
        return {}, 401


@app.route("/api/activities/<string:activity_uuid>", methods=["GET"])
def data_show_activity(activity_uuid):
    data = ShowActivities.run(activity_uuid=activity_uuid)
    return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = "andrewbrown"
    message = request.json["message"]
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/profile/update", methods=["POST", "OPTIONS"])
@cross_origin()
def data_update_profile():
    bio = request.json.get("bio", None)
    display_name = request.json.get("display_name", None)
    try:
        if cognito_verifier.token_is_valid:
            model = UpdateProfile.run(
                cognito_user_id=cognito_verifier.cognito_user_id,
                bio=bio,
                display_name=display_name,
            )
            if model["errors"] is not None:
                return model["errors"], 422
            else:
                return model["data"], 200
        else:
            # unauthenicatied request
            return {}, 401
    except TokenNotFoundException as e:
        print(e)
        return {}, 401


# CloudWatch logging

# @app.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     # LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     return response


with app.app_context():
    def init_rollbar():
        """init rollbar module"""
        rollbar.init(
            # access token
            rollbar_access_token,
            # environment name
            "production",
            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),
            # flask already sets up logging
            allow_logging_basic_config=False,
        )

        # Homework challenge
        # Payload modifier
        def rollbar_payload_handler(payload):
            # Rollbar: adding the user ID to the error
            # generating a random uuid each time.
            user_id = "user-" + str(uuid.uuid4())
            # Add new key/value to the payload
            payload["data"]["user.id"] = user_id
            payload["data"]["user.type"] = random.choice(["standard", "premium"])
            payload["data"]["user.team"] = random.choice(
                ["red team", "blue team", "green team", "yellow team"]
            )
            return payload

        rollbar.events.add_payload_handler(rollbar_payload_handler)

        # send exceptions from `app` to rollbar, using flask's signal system.
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


# @app.route('/rollbar/test')
# def rollbar_test():
#     rollbar.report_message('Hello World!', 'warning')
#     return "Hello World!"


@app.route("/api/users/@<string:handle>/short", methods=["GET"])
def data_users_short(handle):
    data = UsersShort.run(handle)
    return data, 200


if __name__ == "__main__":
    app.run(debug=True)
