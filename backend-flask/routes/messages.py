## flask
from flask import request

## decorators
from flask_cors import cross_origin

## services
from services.message_groups import MessageGroups
from services.messages import Messages
from services.create_message import CreateMessage

## helpers
from lib.helpers import model_json

def load(app, cognito_verifier, telemetry_agent):
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