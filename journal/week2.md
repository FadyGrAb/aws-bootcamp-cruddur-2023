# Week 2 — Distributed Tracing

## Table of Contents

- [Required Homework](#required-homework)
  - [Instrument Honeycomb with OTEL](#instrument-honeycomb-with-otel)
  - [Instrument AWS X-Ray](#instrument-aws-x-ray)
  - [Configure custom logger to send to CloudWatch Logs](#configure-custom-logger-to-send-to-cloudwatch-logs)
  - [Integrate Rollbar and capture an error](#integrate-rollbar-and-capture-an-error)
  - []
- [Homework Challenges](#homework-challenges)
  - [Add custom attributes to Honeycomb and use the queries](#add-custom-attributes-to-honeycomb-and-use-the-queries)
  - [Add custom attributes to Rollbar](#add-custom-attributes-to-rollbar)
  - [Add X-ray segments and metadata](#add-x-ray-segments-and-metadata)
  - [Creating a separate Telemetry module](#creating-a-separate-telemetry-module)

## Required Homework:

### Instrument Honeycomb with OTEL:

I've completed the Honeycomb instrumentation as per the instructions and was able to get the data into Honeycomb.io

- Honeycomb Home visuals for the _bootcamp_ environment:  
  ![home view](assests/week02/req-hw-honeycom01.png)

### Instrument AWS X-Ray:

I was able to instrument AWS X-Ray as follows:

- X-ray deamon logs  
  ![x-ray logs](assests/week02/req-hw-xray-05.png)
- X-ray traces in the cloudWatch UI:  
  ![CloudWatch](assests/week02/req-hw-xray-06.png)  
  ![CloudWatch segments](assests/week02/req-hw-xray-07.png)

### Configure custom logger to send to CloudWatch Logs:

I was able to send the application logs to CloudWatch:  
![CloudWatch](assests/week02/req-hw-cloudwatch-01.png)

### Integrate Rollbar and capture an error:

I have integrated Rollbar and received the warning
![rollbar warning](assests/week02/req-hw-rollbar-01.png)  
And received an error (commented out the return from HomeActivities run function)  
![rollbar error](assests/week02/req-hw-rollbar-02.png)

## Homework Challenges:

### Add custom attributes to Honeycomb and use the queries:

- I've moked-up a span, added attributes to it and viewed it in Honecomb.io:
  ![span](assests/week02/req-hw-honeycom02.png)
- I've used Honeycomb queries:  
  ![Queries](assests/week02/req-hw-honeycom03.png)

### Add custom attributes to Rollbar:

I've searched the [Rollbar official documentation](https://docs.rollbar.com/docs/python#transforming-the-payload) about "_Transforming The Payload_" and managed to add dummy _user_ attributes that randomly change at each request to simulate the real-world app usage. This is done with a _payload handler_ that I've implemented as follows:

```python
def rollbar_payload_handler(payload):
      # Rollbar: adding the user ID to the error
      # generating a random uuid each time.
      import uuid, random
      user_id = "user-" + str(uuid.uuid4())
      payload["data"]["user.id"] = user_id # Add new key/value to the payload
      payload["data"]["user.type"] = random.choice(["standard", "premium"])
      payload["data"]["user.team"] = random.choice(["red team", "blue team", "green team", "yellow team"])
      return payload

# Add handler to rollbar
rollbar.events.add_payload_handler(rollbar_payload_handler)

```

I've added the following attributes:

- user.id
- user.type
- user.team
  I've captured several error occurrences in Rollbar as follows (note the changing values)  
  ![rollbar attr1](assests/week02/hw-ch-rollbar-01.png)  
  ![rollbar attr2](assests/week02/hw-ch-rollbar-02.png)  
  ![rollbar attr3](assests/week02/hw-ch-rollbar-03.png)  
  ![rollbar attr4](assests/week02/hw-ch-rollbar-04.png)  
  ![rollbar attr5](assests/week02/hw-ch-rollbar-05.png)  
  After obtaining the errors, I've fixed the code again to work normally.

### Add X-ray segments and metadata:

I was able to to get x-ray subsegments working reading the [python sdk docs](https://docs.aws.amazon.com/xray-sdk-for-python/latest/reference/basic.html), **Manually create segment/subsegment**. It turned out we don't need to call _begin_segment_ as I assume Flask does that when we hit an endpoint so we only need to call _begin_subsegment_ to record whatever code we need to segment. Also, we have to call _end_subsegment_ to finish the recording and for the record to show in AWS. For the metadata, only a key-value pair is required and we can logically group them by the _namespace_ parameter (it will be '_default_' by default, I've tried it 🙂). The value can be a python dictionary for complex data structures.

```python
subsegment = xray_recorder.begin_subsegment('home-activities-mock-data')

# Code to be recorded goes here.
dict = {
      "now": now.isoformat(),
      "results-size": len(model['data'])
}
subsegment.put_metadata('key', dict, 'namespace')


xray_recorder.end_subsegment()
```

![xray segments](assests/week02/req-hw-xray-08.png)

### Creating a separate Telemetry module:

The main motivation behind this task is that I wanted all the telemetry features introduced into the backend to be controlled from one place. I didn't like the fact that I have to chase pieces of code spread in the entire code base to comment it out/delete to be able to disable the telemetry.  
So, I've created **one** class to control the app's telemetry. It can enable/disable individual feature, pass Rollbar payload handler or disable the telemetry altogether. In case of the telemetry is disabled, all the related telemetry code in the app code base will be ignored and I won't have to delete or comment it.  
Because this is a big change from the original week02 required homework, I've created this task on a different branch [week02-telemetry-module](https://github.com/FadyGrAb/aws-bootcamp-cruddur-2023/tree/week02-telemetry-module/backend-flask) in order not to be confused with the original week02 homework.  
The [telemetry.py](https://github.com/FadyGrAb/aws-bootcamp-cruddur-2023/blob/week02-telemetry-module/backend-flask/telemetry.py) module contains the **Telemetry** class that takes the following params:

```python
class Telemetry:
    def __init__(self, app, honeycomb_active=True, cloudwatch_active=True, xray_active=True,
                    rollbar_active=True, rollbar_payload_handler=None, disable=False):
```

- app: The Flask app instance.
- \*\_active: Where (\*) can be honeycomb, cloudwatch, xray or rollbar. Setting this value to False will disable the corresponding feature. It's True by default for all features.
- rollbar_payload_handler: The payload handler function to modify Rollbar payload data. It takes _payload_ as a parameter which is a dict and returns it after adding key-value pair(s) to its "data" key.
- disabled: If set to True, it will disable all the telemetry features and will ignore all the individual \*\_active flags.

This class follows the same initialization and usage sequences discussed in the video lectures with the main difference that it happens all in one place. This class also wraps the functionality of the original telemetry packages and do nothing when a method is called related to a deactivated feature. Which permits for the telemetry code to remain in the app's code base.

```python
def honeycomb_get_tracer(self, tracer_name):
        if self._honeycomb_trace:   # if honeycomb is disabled, nothing will happen when calling this method.
            return self._honeycomb_trace.get_tracer(tracer_name)
```

To use the class, I have to instantiate it in _app.py_

```python
from telemetry import Telemetry

app = Flask(__name__)

def rollbar_payload_handler(payload):
  ...
  return payload

telemetry_agent = Telemetry(
  app,
  rollbar_payload_handler=rollbar_payload_handler,
  # disable=True
)
```

Then use the instance calling its wrapping methods

```python
class HomeActivities:
  def run(telemetry_agent):
    honeycomb_tracer = telemetry_agent.honeycomb_get_tracer("home-activities-telemetry-module")
    telemetry_agent.cloudwatch_log_info("home-activities-telemetry-module")
    ...
```

I've achieved _identical_ result with all the used services using this class. I've marked the class's logs/traces with the "telemetry-module" suffix.

- Honeycomb
  ![telemetry-module-honeycomb](assests/week02/hw-ch-telemetry-01.png)
- CloudWatch logs
  ![telemetry-module-cloudwatch](assests/week02/hw-ch-telemetry-02.png)
- Rollbar
  ![telemetry-module-rollbar](assests/week02/hw-ch-telemetry-03.png)
- X-ray
  ![telemetry-module-xray](assests/week02/hw-ch-telemetry-04.png)
  I was able to produce the trace in the previous screenshot using a _for loop_ that sleeps for a random amount each iteration and creates a sub-segment.

```python
for i in range (10):
      telemetry_agent.xray_begin_subsegment(f"user_activities_telemetry_module_added_latency_{i}")
      sleep(random.random())
      telemetry_agent.xray_end_subsegment()
```

This isn't an ideal class implementation and I consider it as a POC.
