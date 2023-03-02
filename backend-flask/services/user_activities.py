from datetime import datetime, timedelta, timezone
from time import sleep
import random

class UserActivities:
  def run(user_handle, telemetry_agent):
    # Xray

    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      now = datetime.now()
      results = [{
        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
        'handle':  'Andrew Brown',
        'message': 'Cloud is fun!',
        'created_at': (now - timedelta(days=1)).isoformat(),
        'expires_at': (now + timedelta(days=31)).isoformat()
      }]
      model['data'] = results

      subsegment = telemetry_agent.xray_begin_subsegment('user_activities_telemetry_module_data_mock')
      # xray
      # dict = {
      #   "now": now.isoformat(),
      #   "results-size": len(model['data'])
      # }
      telemetry_agent.xray_add_subsegment_metadata("timestamp", now.isoformat())
      telemetry_agent.xray_add_subsegment_metadata("response-size", len(model['data']))

      telemetry_agent.xray_end_subsegment()

      for i in range (10):
        telemetry_agent.xray_begin_subsegment(f"user_activities_telemetry_module_added_latency_{i}")
        sleep(random.random())
        telemetry_agent.xray_end_subsegment()
      # xray_recorder.end_segment()
    return model