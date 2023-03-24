# Week 5 — DynamoDB and Serverless Caching
## Required Homework:
### Implement Schema Load Script
I've created the *cruddur-messages* table and the *message-group-sk-index* GSI with the *shcema-load* script as instructed.  
![schema load](assests/week05/hwrq-0101-schema-load.gif)
### Implement Seed Script
I've created the seed script with one modification is that instead of using "andrewbrown" as my user and "bayko" as the other user, I used one of my Cognito users "fod" as my user and "other_fady" and the other user. That way I could use the Cognito Update ID script on my data. Also, I've set the base time for the seed messages to be 3 hours in the past so that every new message I create will be in afte the seed messages. Without that, I would have issues displaying the new messages I create if I test it right after the seed.
![seed](assests/week05/hwrq-0201-seed.gif)
### Implement Scan Script
I've created the scan script as instructed.  
![scan](assests/week05/hwrq-0301-scan.gif)
### Implement Pattern Scripts for Read and List Conversations
* The list conversations script
![list conversations](assests/week05/hwrq-0401-list-conversasions.gif)
* The Read conversations script
![get conversation](assests/week05/hwrq-0402-get-conversasion.gif)
### Implement Update Cognito ID Script for Postgres Database
I've implemented the update Cognito ID script.
![cognito update ids](assests/week05/hwrq-0501-update-cognito-id.gif)  
The Cognito user IDs from the console  
![console ids](assests/week05/hwrq-0502-cognito-users.png)
### Implement (Pattern A) Listing Messages in Message Group into Application
I've implemented Pattern A and was able to show the messages from a message group in the app.  
![pattern A](assests/week05/hwrq-0601-list-messages.gif)
### Implement (Pattern B) Listing Messages Group into Application
I've implemented Pattern B and was able list the message groups in the app.  
![pattern B](assests/week05/hwrq-0701-list-message-groups.gif)
### Implement (Pattern C) Creating a Message for an existing Message Group into Application
I was able to create a new message for an *existing* message group (Pattern C) as follows:  
![pattern C](assests/week05/hwrq-0801-create-for-existing.gif)
### Implement (Pattern D) Creating a Message for a new Message Group into Application
I've implemented the "create message for new message groups" (Pattern D) as follows:  
![pattern D](assests/week05/hwrq-0901-create-for-new.gif)
### Implement (Pattern E) Updating a Message Group using DynamoDB Streams
I've created the ddb table and GSI and enabled dynamodb streams (Pattern E):  
![dynamodb streams](assests/week05/hwrq-1001-ddb-streams.png) 
Functionality demo:   
![demo](assests/week05/hwrq-1002-stream-demo.gif)  
The lambda function is envoked without errors:  
![logs](assests/week05/hwrq-1003-stream-lambda-logs.gif)