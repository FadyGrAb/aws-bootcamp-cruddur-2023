# Week 6-7 — Serverless Containers
## Required Homework:
### Provision ECS Cluster:
I've provisioned an ECS cluster throught the AWS console using the default VPC.  
![provision ecs cluster](assests/week0607/hwrq-0101-provision-cluster.png)
### Create ECR repo and push image for backend-flask:
I've created the ***backend-flask*** repo and pushed an image with ***latest*** tag.  
![backend repo](assests/week0607/hwrq-0201-backend-repo.png)
### Deploy Backend Flask app as a service to Fargate:
I've deployed the ***backend-flask*** service after registering the task definition and creating the service through CLI commands.  
![backend service](assests/week0607/hwrq-0301-backend-service.png)
### Create ECR repo and push image for fronted-react-js:
I've created the ***frontend-react-js*** repo and pushed an image with ***latest*** tag.  
![frontend repo](assests/week0607/hwrq-0401-frontend-repo.png)
### Deploy Frontend React JS app as a service to Fargate:
I've deployed the ***frontend-react-js*** service after registering the task definition and creating the service through CLI commands.  
![frontend service](assests/week0607/hwrq-0501-frontend-service.png)
### Provision and configure Application Load Balancer along with target groups:
I've provisined an ALB throught the AWS Console. At its final state, it had only two listiners. One at port 80 which forwards it to port 443 and the other one is on port 443. 
![alb](assests/week0607/hwrq-0601-alb.png)  
I also have provisioned 2 target groups. One for the backend service and the other for the frontend service.  
frontend target group showing healthy state:  
![frontend-tg](assests/week0607/hwrq-0602-frontend-tg.png)  
backend target group showing healthy state:  
![backend-tg](assests/week0607/hwrq-0603-backend-tg.png)  
The ALB has a rule on the 443 port listener as it forwards the request to the backend target group if the domain URL starts with ***api*** otherwise forwards it to the frontend target group.
![443 rule](assests/week0607/hwrq-0604-rule.png)  
I also managed to export the ALB Access logs to S3 using this S3 bucket policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::127311923021:root"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::cruddur-alb-access-logs-fm/*"
        }
    ]
}
```
But it turned out that it burns through S3 Free Tier requests so I've disabled it later.
### Manage your domain using Route53 via hosted zone:
In Amazon Route53, I've a hosted zone for my domain (it was created by default as I purchashed my domain from AWS).  
![hosted zone](assests/week0607/hwrq-0701-hostedzones.png)  

Demo for using Cruddur over my domain:  
![domain demo](assests/week0607/hwrq-0702-domain-demo.gif)
### Create an SSL cerificate via ACM:
I've created the SSL manually through the AWS Console in Certificates Manager.  
![hosted zone](assests/week0607/hwrq-0801-ssl.png)
### Setup a record set for naked domain to point to frontend-react-js:
In Amazon Route53, I've created an A record to forward the requests comming to the naked domain to the ALB. The ALB will forward the requests to the frontend target group as the condition for the 443 listener is not met.  
![naked domain](assests/week0607/hwrq-0901-naked-domain.png)
### Setup a record set for api subdomain to point to the backend-flask:
In Amazon Route53, I've created an A record to forward the requests comming to the api subdomain to the ALB. The ALB will forward the requests to the backend target group as the condition for the 443 listener is met.  
![naked domain](assests/week0607/hwrq-1001-api-domain.png)
### Configure CORS to only permit traffic from our domain:
I've set the BACKEND_URL env var to my api sub-domain and FRONTEND_URL env var to my naked domain for the ***backend-flask*** container which should configure the app's CORS to just my domain.
![cors](assests/week0607/hwrq-1101-backend-cros.png)  
### Secure Flask by not running in debug mode:
I've used *--no-debug*, *--no-debugger*, *--no-reload* options in the flask command whithin the dockerfile of the backend. Furthermore, I've confirmed that by connecting to the ***backend-flask*** container, running `flask shell` to get a python shell with the app context and finally checking on the value for ***app.debug*** which was False.  
![securing flask](assests/week0607/hwrq-1201-secure-flask.png)
### Implement Refresh Token for Amazon Cognito:
I've implemented the refresh token and made the necessary changes. I've tried to post a message after aproximattly 3 hours from signing in and I did that without issues but I couldn't think of a way to properly documment that.
```js
// lib/CheckAuth.js
import { Auth } from "aws-amplify";

async function getAccessToken() {
  Auth.currentSession()
    .then((cognito_user_session) => {
      const access_token = cognito_user_session.accessToken.jwtToken;
      localStorage.setItem("access_token", access_token);
    })
    .catch((err) => console.log(err));
}

async function checkAuth(setUser) {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false.
    // If set to true, this call will send a
    // request to Cognito to get the latest user data
    bypassCache: false,
  })
    .then((cognito_user) => {
      console.log("cognito_user", cognito_user);
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username,
      });
      return Auth.currentSession();
    })
    .then((cognito_user_session) => {
      console.log("cognito_user_session", cognito_user_session);
      localStorage.setItem(
        "access_token",
        cognito_user_session.accessToken.jwtToken
      );
    })
    .catch((err) => console.log(err));
}

export { checkAuth, getAccessToken };

```
### Refactor bin directory to be top level:
I've recactored the bin directory. I ocasionally open up the project on my local windows machine and I have created some scripts of my own that uses *Powershell* in the ***_mine*** directory but I excluded those from being committed.  
![bin refactoring](assests/week0607/hwrq-1401-bin.png)
### Configure task defintions to contain x-ray and turn on Container Insights:
I've truned on "***Container Insights***" and included x-ray for each service.  
x-ray containers in the services:  
* Backend
![backend x-ray](assests/week0607/hwrq-1501-backend.png)
* Frontend
![frontend x-ray](assests/week0607/hwrq-1502-frontend.png)
* Cognito Verifier Sidecar
![cognito verifier x-ray](assests/week0607/hwrq-1503-frontend.png)  

Turning on ***Container Insights***:
![Container Insights](assests/week0607/hwrq-1504-container-insights.png)  
![Container Insights](assests/week0607/hwrq-1505-container-insights.png)  
### Change Docker Compose to explicitly use a user-defined network:
I've made the required changes and tested it.  
1- Made sure that all the containers are running after a `docker compose up -d` command  
![all containers](assests/week0607/hwrq-1601-all-containers.png)  
2- Check for docker networks using `docker network list --all`. The user defined network ***cruddur-net*** exists.  
![all networks](assests/week0607/hwrq-1602-list-all-networks.png)  
3- Inspecting the ***cruddur-net*** user defined network and see which containers are using it. Using `docker network inspect cruddur-net | jq .[0].Containers` to only show the containers part, confirms that the network is used by the docker-compose conatainers.  
![network inspect](assests/week0607/hwrq-1603-network-inspect.png)  

### Create Dockerfile specfically for production use case:
I've created a production Dockerfile for both the backend and frontend.  
![Dockerfile backend](assests/week0607/hwrq-1701-dockerfile-backend.png)  
![Dockerfile backend](assests/week0607/hwrq-1702-dockerfile-frontend.png)  
### Using ruby generate out env dot files for docker using erb templates:
I've created the needed ruby scripts and erb templates. But instead of using `source` in the ***.gitpod.yml*** to run them, I've use `ruby /path/to/ruby/script` as those are ruby scripts and source is used for bash scripts. The files are generated once I get in my Gitpod environment.  
![env vars](assests//week0607/hwrq-1801-ruby.png)  
## Homework challenges:
### Running my cognito sidecar as a 3rd service:
I've created a 3rd service for my sidecar implementation of ***Cognito Verifier*** following the same porcess for the backend and fronten services but this one doesn't belong to any target group. The way my ***backend-flask*** communicates with it is through the internal DNS that Service Connect creates. I had to do some research and some trials to figure out this DNS name but I finally figured it out. In my case it was `http://container-name.cluster-name`.  

cognito-verifier sidecar ECR repos:  
![repo](assests/week0607/hwch-0101-ecr-repos.png)
cognito-verifier running task:  
![task](assests/week0607/hwch-0102-task.png)

