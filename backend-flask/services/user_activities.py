# from datetime import datetime, timedelta, timezone
# from aws_xray_sdk.core import xray_recorder

from lib.db import db


class UserActivities:
    def run(user_handle):
        # Xray

        model = {
            'errors': None,
            'data': None
        }

        if user_handle == None or len(user_handle) < 1:
            model['errors'] = ['blank_user_handle']
        else:
            sql = db.template('users', 'show')
            results = db.query_object_json(sql, {'handle': user_handle})
            model['data'] = results

            # subsegment = xray_recorder.begin_subsegment('home-activities-mock-data')
            # # xray
            # dict = {
            #   "now": now.isoformat(),
            #   "results-size": len(model['data'])
            # }
            # subsegment.put_metadata('key', dict, 'namespace')
            # xray_recorder.end_subsegment()

            # X-ray subsegments
            # subsegment = xray_recorder.begin_subsegment('user_activities_data_mock')

            # # Add subsegment metadata
            # xray_recorder.put_metadata("timestamp", now.isoformat())
            # xray_recorder.put_metadata("response-size", len(model['data']))

            # xray_recorder.end_subsegment()

        return model
