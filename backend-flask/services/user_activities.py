from datetime import datetime, timedelta, timezone
from time import sleep
import random

from lib.db import db

class UserActivities:
    def run(user_handle, telemetry_agent):
        # Xray

        model = {
            'errors': None,
            'data': None
        }

        if user_handle == None or len(user_handle) < 1:
            model['errors'] = ['blank_user_handle']
        else:
            sql = db.get_template('users', 'show')
            results = db.query_object_json(sql, {'handle': user_handle})
            model['data'] = results

            # X-ray subsegments
            now = datetime.now(timezone.utc).astimezone()
            subsegment = telemetry_agent.xray_begin_subsegment('user_activities_telemetry_module_data_mock')
      
            telemetry_agent.xray_add_subsegment_metadata("timestamp", now.isoformat())
            telemetry_agent.xray_add_subsegment_metadata("response-size", len(model['data']))

            telemetry_agent.xray_end_subsegment()

            for i in range (10):
                telemetry_agent.xray_begin_subsegment(f"user_activities_telemetry_module_added_latency_{i}")
                sleep(random.random())
                telemetry_agent.xray_end_subsegment()

        return model
