# Week 2 — Distributed Tracing

## Required Homework:
### Instrument Honeycomb with OTEL:
I've completed the Honeycomb instrumentation as per the instructions and was able to get the data into Honeycomb.io  
* Honeycomb Home visuals for the *bootcamp* environment:  
![home view](assests/week02/req-hw-honeycom01.png)  
* Moked-up a span, added attributes to it and viewed it in Honecomb.io: 
![span](assests/week02/req-hw-honeycom02.png)  
* Used Honeycomb queries:  
![Queries](assests/week02/req-hw-honeycom03.png)  

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