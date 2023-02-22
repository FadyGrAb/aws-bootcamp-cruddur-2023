# Week 1 — App Containerization

## Required Homework:
### Containerize Application (Dockerfiles, Docker Compose)
I've built the backend and frontend containers using Dockerfile  
Running backend-flask (build from Dockerfile)
![backend dockerfile](assests/week01/reqhw-dockerize-backend-dockerfile.png)  
/api/activities/home response  
![backend response](assests/week01/reqhw-dockerize-backend-dockerfile%2002.png)
   
    
Runing frontend-react-js (build from Dockerfile)
![frontend dockerfile](assests/week01/reqhw-dockerize-frontend-dockerfile%2001.png)
Frontend page
![frontend page](assests/week01/reqhw-dockerize-frontend-dockerfile%2002.png)

And with docker compose
![docker compose](assets/week01/../../assests/week01/reqhw-dockerize-dockercompose%2001.png)

Frontend while running with docker compose using the backend API
![docker compose frontend and backend](assests/week01/reqhw-dockerize-dockercompose%2002.png)

### Document the Notification Endpoint for the OpenAPI Document:
![OpenAPI documentation](assests/week01/reqhw-open-api%2001.png)

### Write a Flask Backend Endpoint for Notifications:
Result for the new nofications endpoint
![notifications backend](assests/week01/reqhw-notificaitons-backend%2001.png)

### Write a React Page for Notifications:
![notifications frontend](assests/week01/reqhw-notificaitons-frontend%2001.png)

### Run DynamoDB Local Container and ensure it works:
Running `docker compose ps` after `docker compose up -d` to see all the running containers. The DynamomDB container (and postgres container) are highligted.
![DynamoDB and postgress containers](assests/week01/reqhw-dynamodb-postgres%2001.png)
<br>
And to ensure that dynamodb is working, I've created the table and added the item as in the instructions then listed them out.
![Listing dynamodb table and items](assests/week01/reqhw-dynamodb-postgres%2002.png)

### Run Postgres Container and ensure it works:
As for postges, I've logged in as the '*postgres*' user as instructed and listed all the databases in the db with `\l`.
![databases in postgres](assests/week01/reqhw-dynamodb-postgres%2003.png)

## Homework chalenges:
### Intalling Docker on my local machine and running the same containers:

I've installed Docker Desktop on windows on my local enviornment and ran the containers.  
Running docker from vscode's terminal:
![vscode docker](assests/week01/hwcl-01.png)
Docker desktop on Windows:
![docker desktop](assests/week01/hwcl-02.png)


