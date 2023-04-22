# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy
## Required Homework:
### Configuring CodeBuild:
I've configured CodeBuild as per the video instructions (1 and 2) and I made sure it ran successfully. I had some minor difficulties getting CodeBuild to build the image as I switched the build command to use `Dockerfile.prod` instead of the `Dockerfile` in the instructions. And as this file uses some build args, I had to make the necessary adjustments in the `buildspecs.yml`. Also, I tried to pass ***AWS_ACCOUNT_ID*** from the CodePipeline through AWS Console click-ops as I didn't want to pass it in the `buildspecs.yml`, eventually I got it working by using 
```sh
export IMAGE_URL="$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
``` 
in `buildspecs.yml`.
* Build project configs:
![project](assests/week09/hwreq-0101-codebuild-config.png)
* Source configs:
![Source](assests/week09/hwreq-0102-codebuild-config-source.png)
* Environment configs:
![Environment](assests/week09/hwreq-0103-codebuild-config-env.png)
* Buildspecs configs:
![Buildspecs](assests/week09/hwreq-0104-codebuild-config-buildspec.png)
* Logs configs:
![Logs](assests/week09/hwreq-0105-codebuild-config-logs.png)
### Configuring CodePipeline:
I've configured the CodePipeline and integrated the CodeBuild project just configured.  
* Source configs:
![Source](assests/week09/hwreq-0201-codepipline-config-source.png)
* Build configs:
![Build](assests/week09/hwreq-0202-codepipline-config-build.png)
* Deploy configs:
![Deploy](assests/week09/hwreq-0203-codepipline-config-deploy.png)
* Successful pipeline run:
![Successful run](assests/week09/hwreq-0204-successful-deployment.png)
* Pipeline run demo:
![pipeline run](assests/week09/hwreq-0206-codepipeline-demo.gif)
* Api health check before the deployment (shows ver 1):
![before build](assests/week09/hwreq-0204-before-deployment.png)
* Api health check after the deployment (shows ver 2):
![before build](assests/week09/hwreq-0205-after-deployment.png)