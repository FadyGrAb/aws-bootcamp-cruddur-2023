import os
import uuid
import random

def model_json(model):
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200

def rollbar_payload_handler(payload):
  # Example rollbar payload modifier  
  payload["data"]["user.id"] = "user-" + str(uuid4())
  payload["data"]["user.type"] = random.choice(["standard", "premium"])
  payload["data"]["user.team"] = random.choice(["red team", "blue team", "green team", "yellow team"])
  payload["data"]["module_tag"] = "telemetry-module"
  return payload