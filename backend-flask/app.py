from flask import Flask

import routes.activities
import routes.general
import routes.users
import routes.messages

from lib.telemetry import Telemetry
from lib.cognito_verifier_middleware import CognitoVerifierMiddleware
from lib.cognito_verifier_middleware.exceptions import *
from lib.helpers import rollbar_payload_handler, model_json
from lib.cors import init_cors

app = Flask(__name__)

# Initalization
telemetry_agent = Telemetry(
  app,
  rollbar_payload_handler=rollbar_payload_handler,
  xray_active=False
)
cognito_verifier = CognitoVerifierMiddleware(app)
cors = init_cors(app)

# Load routes
routes.activities.load(app, cognito_verifier, telemetry_agent)
routes.general.load(app)
routes.users.load(app, cognito_verifier, telemetry_agent)
routes.messages.load(app, cognito_verifier, telemetry_agent)


# @app.route("/api/activities/<string:activity_uuid>", methods=["GET"])
# def data_show_activity(activity_uuid):
#     data = ShowActivities.run(activity_uuid=activity_uuid)
#     return data, 200


if __name__ == "__main__":
    app.run(debug=True)
