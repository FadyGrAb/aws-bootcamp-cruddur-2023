## flask
from flask import request

## decorators
from flask_cors import cross_origin

## services
from services.home_activities import HomeActivities
from services.notifications_activities import NotifictionsActivities
from services.create_activity import CreateActivity
from services.search_activities import SearchActivities
from services.create_reply import CreateReply

from lib.helpers import *

def load(app, cognito_verifier=None, telemetry_agent=None):
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

    @app.route("/api/activities/search", methods=["GET"])
    def data_search():
        term = request.args.get("term")
        model = SearchActivities.run(term)
        return model_json(model)

    @app.route("/api/activities", methods=["POST", "OPTIONS"])
    @cross_origin()
    def data_activities():
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

    @app.route("/api/activities/<string:activity_uuid>/reply", methods=["POST", "OPTIONS"])
    @cross_origin()
    def data_activities_reply(activity_uuid):
        user_handle = "andrewbrown"
        message = request.json["message"]
        model = CreateReply.run(message, user_handle, activity_uuid)
        return model_json(model)

