# Week 2 — Distributed Tracing

## Required Homework:
### Instrument Honeycomb with OTEL:
I've completed the Honeycomb instrumentation as per the instructions and was able to get the data into Honeycomb.io  
* Honeycomb Home visuals for the *bootcamp* environment:  
![home view](assests/week02/req-hw-honeycom01.png)  


### Instrument AWS X-Ray:
I was able to instrument AWS X-Ray as follows:  
* X-ray deamon logs  
![x-ray logs](assests/week02/req-hw-xray-05.png)  
* X-ray traces in the cloudWatch UI:  
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
* I've moked-up a span, added attributes to it and viewed it in Honecomb.io: 
![span](assests/week02/req-hw-honeycom02.png)  
* I've used Honeycomb queries:  
![Queries](assests/week02/req-hw-honeycom03.png)  

### Add custom attributes to Rollarbar:
I've searched the [Rollbar official documentation](https://docs.rollbar.com/docs/python#transforming-the-payload) about "*Transforming The Payload*" and managed to add dummy *user* attributes that randomly change at each request to simulate the real-world app usage. This is done with a *payload handler* that I've implimented as follows:
```python
def rollbar_payload_handler(payload): # kw is currently unused
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
* user.id
* user.type
* user.team
I've captured several error occurences in Rollarbar as follows (note the changing values)  
![rollbar attr1](assests/week02/hw-ch-rollbar-01.png)  
![rollbar attr2](assests/week02/hw-ch-rollbar-02.png)  
![rollbar attr3](assests/week02/hw-ch-rollbar-03.png)  
![rollbar attr4](assests/week02/hw-ch-rollbar-04.png)  
![rollbar attr5](assests/week02/hw-ch-rollbar-05.png)  
After obtaining the errors, I've fixed the code again to work normally.

