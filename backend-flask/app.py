import os
import uuid
import random

from flask import abort, make_response, jsonify
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

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

from lib.telemetry import Telemetry
from lib.cognito_verifier_middleware import CognitoVerifierMiddleware
from lib.cognito_verifier_middleware.exceptions import *
from lib.heplers import *
from lib.cors import init_cors

def rollbar_payload_handler(payload):
  # Example rollbar payload modifier  
  payload["data"]["user.id"] = "user-" + str(uuid4())
  payload["data"]["user.type"] = choice(["standard", "premium"])
  payload["data"]["user.team"] = choice(["red team", "blue team", "green team", "yellow team"])
  payload["data"]["module_tag"] = "telemetry-module"
  return payload

app = Flask(__name__)

# Init my Telemetry module
telemetry_agent = Telemetry(
  app,
  rollbar_payload_handler=rollbar_payload_handler,
  xray_active=False
)

# Init my cognito middleware
cognito_verifier = CognitoVerifierMiddleware(app)

# Init CORS
cors = init_cors(app)

@app.route("/api/health-check")
def health_check():
    return {"success": True, "ver": 2}, 200


@app.route("/api/message_groups", methods=["GET"])
def data_message_groups():
    try:
        if cognito_verifier.token_is_valid:
            model = MessageGroups.run(cognito_user_id=cognito_verifier.cognito_user_id)
            return model_json(model)
        else:
            return {}, 401
    except TokenNotFoundException as e:
        print(e)
        return {}, 401


@app.route("/api/messages/<string:message_group_uuid>", methods=["GET"])
def data_messages(message_group_uuid):
    try:
        if cognito_verifier.token_is_valid:
            model = Messages.run(
                message_group_uuid=message_group_uuid,
                cognito_user_id=cognito_verifier.cognito_user_id,
            )
            return model_json(model)
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
            return model_json(model)
        else:
            return {}, 401
    except TokenNotFoundException as e:
        print(e)
        return {}, 401


@app.route("/api/activities/home", methods=["GET"])
def data_home():
    # My cognito middleware implementation
    if cognito_verifier.token_is_valid:
        cognito_user_id = cognito_verifier.cognito_user_id
        data = HomeActivities.run(cognito_user_id=cognito_user_id, telemetry_agent=telemetry_agent)
    else:
        data = HomeActivities.run(telemetry_agent=telemetry_agent)
    return data, 200


@app.route("/api/activities/notifications", methods=["GET"])
def data_notifications():
    data = NotifictionsActivities.run()
    return data, 200


@app.route("/api/activities/@<string:handle>", methods=["GET"])
def data_handle(handle):
    model = UserActivities.run(handle, telemetry_agent)
    return model_json(model)


@app.route("/api/activities/search", methods=["GET"])
def data_search():
    term = request.args.get("term")
    model = SearchActivities.run(term)
    return model_json(model)


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
            return model_json(model)
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
    return model_json(model)



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
            return model_json(model)

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
