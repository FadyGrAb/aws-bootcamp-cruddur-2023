# Week 1 — App Containerization

## Table of Contents

- [Required Homework](#required-homework)
  - [Containerize Application (Dockerfiles, Docker Compose)](#containerize-application-dockerfiles-docker-compose)
  - [Document the Notification Endpoint for the OpenAPI Document](#document-the-notification-endpoint-for-the-openapi-document)
  - [Write a Flask Backend Endpoint for Notifications](#write-a-flask-backend-endpoint-for-notifications)
  - [Write a React Page for Notifications](#write-a-react-page-for-notifications)
  - [Run DynamoDB Local Container and ensure it works](#run-dynamodb-local-container-and-ensure-it-works)
  - [Run Postgres Container and ensure it works](#run-postgres-container-and-ensure-it-works)
- [Homework Challenges](#homework-challenges)
  - [Installing Docker on my local machine and running the same containers](#installing-docker-on-my-local-machine-and-running-the-same-containers)
  - [Reviewed docker build best practice](#reviewed-docker-build-best-practice)
  - [Building a "_Hello World_" flask app locally](#building-a-hello-world-flask-app-locally)
  - [Dockerize the **flask-docker** app and test it from docker](#dockerize-the-flask-docker-app-and-test-it-from-docker)
  - [Pushing the image to DockerHub](#pushing-the-image-to-dockerhub)
  - [Pulling the image from an EC2](#pulling-the-image-from-an-ec2)
  - [Trying to reduce the image size and pushing it back to docker hub](#trying-to-reduce-the-image-size-and-pushing-it-back-to-docker-hub)
  - [Further reducing the image size](#further-reducing-the-image-size)

## Required Homework:

### Containerize Application (Dockerfiles, Docker Compose)

I've built the backend and frontend containers using Dockerfile

- Running backend-flask (build from Dockerfile)
  ![backend dockerfile](assests/week01/reqhw-dockerize-backend-dockerfile.png)
- /api/activities/home response  
  ![backend response](assests/week01/reqhw-dockerize-backend-dockerfile%2002.png)
- Runing frontend-react-js (build from Dockerfile)
  ![frontend dockerfile](assests/week01/reqhw-dockerize-frontend-dockerfile%2001.png)
- Frontend page
  ![frontend page](assests/week01/reqhw-dockerize-frontend-dockerfile%2002.png)

- And with docker compose
  ![docker compose](assets/week01/../../assests/week01/reqhw-dockerize-dockercompose%2001.png)

- Frontend while running with docker compose using the backend API
  ![docker compose frontend and backend](assests/week01/reqhw-dockerize-dockercompose%2002.png)

### Document the Notification Endpoint for the OpenAPI Document:

![OpenAPI documentation](assests/week01/reqhw-open-api%2001.png)

### Write a Flask Backend Endpoint for Notifications:

- Result for the new notifications endpoint
  ![notifications backend](assests/week01/reqhw-notificaitons-backend%2001.png)

### Write a React Page for Notifications:

![notifications frontend](assests/week01/reqhw-notificaitons-frontend%2001.png)

### Run DynamoDB Local Container and ensure it works:

Running `docker compose ps` after `docker compose up -d` to see all the running containers. The DynamomDB container (and postgres container) are highlighted.
![DynamoDB and postgress containers](assests/week01/reqhw-dynamodb-postgres%2001.png)
<br>
And to ensure that dynamodb is working, I've created the table and added the item as in the instructions then listed them out.
![Listing dynamodb table and items](assests/week01/reqhw-dynamodb-postgres%2002.png)

### Run Postgres Container and ensure it works:

As for postges, I've logged in as the '_postgres_' user as instructed and listed all the databases in the db with `\l`.
![databases in postgres](assests/week01/reqhw-dynamodb-postgres%2003.png)

## Homework challenges:

### Installing Docker on my local machine and running the same containers:

I've installed Docker Desktop on windows on my local environment and ran the containers.

- Running docker from vscode's terminal:
  ![vscode docker](assests/week01/hwcl-01.png)
- Docker desktop on Windows:
  ![docker desktop](assests/week01/hwcl-02.png)

### Reviewed docker build best practice:

I've checked out this [doc page](https://docs.docker.com/engine/reference/builder/#dockerignore-file) and tried to apply the image size reductions tactics next.

### Building a "_Hello World_" flask app locally:

I have created a very simple flask app having only one root endpoint "/" with the intention to dockerize it and push it to DockerHub then pulling it back from an EC2 ([App repo](https://github.com/FadyGrAb/aws-bootcamp-docker-flask-app)).  
I tested the app locally without docker and launched the app on port 8888

```console
flask run --host=0.0.0.0 --port=8888
```

- Flask dev server and response (without docker)
  ![flask dev server](assests/week01/hwcl-testing-flaskapp-locally-01.png)
- Browser Response (actually now it isn't form docker, yet 😉)  
  ![flask app from browser](assests/week01/hwcl-testing-flaskapp-locally-02.png)

### Dockerize the **flask-docker** app and test it from docker:

I've created a [Dockerfile](https://github.com/FadyGrAb/aws-bootcamp-docker-flask-app/blob/main/Dockerfile) for the app to run on the container on port 8080.

```console
docker build -t flask-docker:demo .
```

![Docker build successful](assests/week01/hwcl-dockerize-and-test-flask-docker-app-01.png)  
Then I ran the app as a container and tested it.

```console
docker run --rm -p 8080:8080 -it flask-docker:demo
```

- Flask dev server from docker
  ![flask dev server from docker](assests/week01/hwcl-dockerize-and-test-flask-docker-app-02.png)
- Browser page (from docker this time 🙂)  
  ![docker browser page](assests/week01/hwcl-dockerize-and-test-flask-docker-app-03.png)

### Pushing the image to DockerHub:

In order to push the image, I've followed the next steps (as described in the docs [here](https://docs.docker.com/engine/reference/commandline/push/) and [here](https://docs.docker.com/docker-hub/repos/)):

- login to DockerHub from the CLI

```console
docker login
```

![docker hub login](assests/week01/hwcl-push-docker-image-01.png)

- Tag the flask-docker app image to match my DockerHub ID

```console
docker image tag flask-docker:demo fadygrab/flask-docker:demo
```

![tagging the image](assests/week01/hwcl-push-docker-image-02.png)

- And finally pushing the image to the [DockerHub repo]()

```console
docker image push fadygrab/flask-docker:demo
```

![image pushed](assests/week01/hwcl-push-docker-image-03.png)
![image pushed](assests/week01/hwcl-push-docker-image-04.png)

## Pulling the image from an EC2:

I've performed the following:

- Provision an EC2 with a Role of DicrectConnect FullAccess to be able to access from the AWS portal directly.
  ![EC2](assests/week01/hwcl-ec2-test-01.png)
- Install and start docker on EC2 (I have some previous experience with that).

```
sudo yum update
sudo yum install docker
sudo systemctl start docker
```

![docker started on EC2](assests/week01/hwcl-ec2-test-02.png)

- Pull the image.  
  ![image pulled](assets/../assests/week01/hwcl-ec2-test-03.png)
- Run a container.  
  ![container running](assests/week01/hwcl-ec2-test-04.png)
- And finally tested it with `curl` command. And it worked 🥳  
  ![image is working on EC2](assests/week01/hwcl-ec2-test-05.png)  
  The 200 status code and the "_Hello from flask within docker_" response!

## Trying to reduce the image size and pushing it back to docker hub:

I've researched the topic of how to achieve a small image. Some of the tactics were to use minimal base images and purge any cached file for the pip (if used) and package manager. I've tried those and achieved almost 28% size reduction of the overall image size (in my local environment). Then I have committed the changes to the docker hub repo.

- Creating a new docker file with the below changes
  - Changing the base image form `python:3.10.10-slim-bullseye` to `python:3.10.10-alpine3.17`
  - Purged the pip cache in the same `RUN` layer to install the requirements to reduce the layers count `RUN pip3 install -r requirements && pip3 cache purge`(another optimization tactic).
- I've built the new image form the new [dockerfile](https://github.com/FadyGrAb/aws-bootcamp-docker-flask-app/blob/main/Dockerfile.v1) and almost 75MB size reduction is achieved.

```powershell
docker build -t flask-docker:v1 -f ./Dockervile.v1 .        # The -f option is to override the default Dockerfile
```

![image reduced size](assests/week01/hwcl-reduce-size-01.png)

- Then I've retested the new image just to be sure 😉
  1. Run the container.
  2. Test the endpoint with `curl` command (to save a bit of time 😁) and I goth the "_Hello from flask within docker_" phrase.
  3. And I got the 200 status code.
  4. Stopped the container.
  5. Made sure that the container doesn't exist anymore.

Used commands:

```powershell
docker run --rm -p 8080:8080 -d flask-docker:v1     # Run the container.
docker container list                               # List the running containers.
curl [-I] http://localhost:8080                     # Get the endpoint's response. (curl must be installed in order to work. I use the executable from my local git installation on Windows)
docker container stop <container id>                # Stopping the container.
docker container list --all                         # Making sure that the container is stopped.
```

![testing the new image](assests/week01/hwcl-reduce-size-02.png)

- And finally performing the same procedure to push the new image to the DockerHub repo after tagging the new image using the following steps:
  1. Listing the current images in my local environment.
  2. Tagging the new image with my DockerHub user name.
  3. Pushing the new image.
  4. Listing the images again to see the new tag just as sanity check.

Used commands:

```powershell
docker image list                                       # List the available images locally.
docker tag flask-docker:v1 fadygrab/flask-docker:v1     # Tagging the image to match my DcokerHub repo username.
docker image push fadygrab/flask-docker:v1              # Pushing the new image to the repo.
docker image list                                       # Sanity-check.
```

![push the new image](assests/week01/hwcl-reduce-size-03.png)  
The new image on DockerHub 👇
![the new image on dockerhub](assests/week01/hwcl-reduce-size-04png.png)

## Further reducing the image size:

I've created a virtual python environment on my local machine (when I was testing the app) and it turned out that the `COPY . /flask-docker-demo/ ` was copying EVERYTHING in the root folder including the git history, the venv files and dockerfiles. And as another best practice, I've used [.dockerignore](https://github.com/FadyGrAb/aws-bootcamp-docker-flask-app/blob/main/.dockerignore) to exclude all the files/folders I don't need (I could have just modified the copy layer to be `COPY app.py requirements /flask-docker-demo/` and it would have just worked the same but I wanted to used .dockerignore).  
So again I build the v2 image (but tagged it directly to DockerHub user name) and this time I've achieved 78% size reduction from the original size and 69% size reduction for V1.  
I've followed the next steps:

1. Re-build the image this time with a .dockerignore inplace and tagging the image to match the dockerhub user on the fly.
2. See the resulting images size (69% reduction from v1).
3. Run a container with V2 image.
4. Test that container with `curl` command and I got the "_Hello form flask within docker_" statement.
5. Stop the container.
6. Push the v2 image to the DockerHub repo.

![further size reduction](assests/week01/hwcl-reduce-size-05png.png)  
And the v2 image is also on docker hub too  
![v2 on dockerhub](assests/week01/hwcl-reduce-size-06.png)
