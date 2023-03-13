from datetime import datetime, timedelta, timezone
from opentelemetry import trace

from lib.db import pool, query_wrap_array

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(cognito_user_id=None, logger=None):
    if logger:
      # Cloudwatch Logging goes here
      # logger.info("home-activities")
      pass

    with tracer.start_as_current_span("home-activities-mock-data"):
      # Get the current span
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())

      # results = [{
      #   'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      #   'handle':  'Andrew Brown',
      #   'message': 'Cloud is very fun!',
      #   'created_at': (now - timedelta(days=2)).isoformat(),
      #   'expires_at': (now + timedelta(days=5)).isoformat(),
      #   'likes_count': 5,
      #   'replies_count': 1,
      #   'reposts_count': 0,
      #   'replies': [{
      #     'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
      #     'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      #     'handle':  'Worf',
      #     'message': 'This post has no honor!',
      #     'likes_count': 0,
      #     'replies_count': 0,
      #     'reposts_count': 0,
      #     'created_at': (now - timedelta(days=2)).isoformat()
      #   }],
      # },
      # {
      #   'uuid': '66e12864-8c26-4c3a-9658-95a10f8fea67',
      #   'handle':  'Worf',
      #   'message': 'I am out of prune juice',
      #   'created_at': (now - timedelta(days=7)).isoformat(),
      #   'expires_at': (now + timedelta(days=9)).isoformat(),
      #   'likes': 0,
      #   'replies': []
      # },
      # {
      #   'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
      #   'handle':  'Garek',
      #   'message': 'My dear doctor, I am just simple tailor',
      #   'created_at': (now - timedelta(hours=1)).isoformat(),
      #   'expires_at': (now + timedelta(hours=12)).isoformat(),
      #   'likes': 0,
      #   'replies': []
      # }
      # ]

      # span.set_attribute("app.result.length", len(results))
      
      # if cognito_user_id:
      #   results.insert(
      #     0, 
      #     {
      #       'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
      #       'handle':  cognito_user_id,
      #       'message': "I'm logged in!",
      #       'created_at': (now - timedelta(hours=1)).isoformat(),
      #       'expires_at': (now + timedelta(hours=12)).isoformat(),
      #       'likes': 0,
      #       'replies': []
      #     }
      #   )

      sql = query_wrap_array("""
        SELECT
          activities.uuid,
          users.display_name,
          users.handle,
          activities.message,
          activities.replies_count,
          activities.reposts_count,
          activities.likes_count,
          activities.reply_to_activity_uuid,
          activities.expires_at,
          activities.created_at
        FROM public.activities
        LEFT JOIN public.users ON users.uuid = activities.user_uuid
        ORDER BY activities.created_at DESC
      """)
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchall()

      # print("respose =====>\n",json[0][0], flush=True)
    return json[0][0]