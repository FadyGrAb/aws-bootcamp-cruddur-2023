# Week 5 — DynamoDB and Serverless Caching
## Required Homework:
### Implement Schema Load Script
I've created the *cruddur-messages* table and the *message-group-sk-index* GSI with the *shcema-load* script as instructed.  
DEMO GIF GOES HERE
### Implement Seed Script
I've created the seed script with one modification is that instead of using "andrewbrown" as my user and "bayko" as the other user, I used one of my Cognito users "fod" as my user and "other_fady" and the other user. That way I could use the Cognito Update ID script on my data.  
DEMO GIF GOES HERE
### Implement Scan Script
I've created the scan script as instructed.  
DEMO GIF GOES HERE
### Implement Pattern Scripts for Read and List Conversations
* The list conversations script
DEMO GIF GOES HERE
* The Read conversations script
DEMO GIF GOES HERE
### Implement Update Cognito ID Script for Postgres Database
I've implemented the update Cognito ID script.
DEMO GIF GOES HERE
COGNITO USER PIC GOES HERE
### Implement (Pattern A) Listing Messages in Message Group into Application
I've implemented Pattern A and was able to show the messages from a message group in the app.  
DEMO GIF GOES HERE
### Implement (Pattern B) Listing Messages Group into Application
I've implemented Pattern B and was able list the message groups in the app.  
DEMO GIF GOES HERE
### Implement (Pattern C) Creating a Message for an existing Message Group into Application
I was able to create a new message for an *existing* message group as follows:  
DEMO GIF GOES HERE
### Implement (Pattern D) Creating a Message for a new Message Group into Application
### Implement (Pattern E) Updating a Message Group using DynamoDB Streams