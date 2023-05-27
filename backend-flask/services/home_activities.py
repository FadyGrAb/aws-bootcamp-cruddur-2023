from datetime import datetime, timedelta, timezone
from opentelemetry import trace

# from lib.db import pool, query_wrap_array
from lib.db import db

class HomeActivities:
  def run(cognito_user_id=None, telemetry_agent=None):
    if telemetry_agent:
      # Cloudwatch Logging goes here
      telemetry_agent.cloudwatch_log_info("home-activities")
      honeycomb_tracer = telemetry_agent.honeycomb_get_tracer("home-activities-telemetry-module")
      
    if honeycomb_tracer:
      with honeycomb_tracer.start_as_current_span("home-activities-mock-data"):
        # Get the current span
        span = trace.get_current_span()
        now = datetime.now(timezone.utc).astimezone()
        span.set_attribute("app.now", now.isoformat())

        sql = db.get_template('activities','home')
        results = db.query_array_json(sql)
    else:
      sql = db.get_template('activities','home')
      results = db.query_array_json(sql)
    
    return results