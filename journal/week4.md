# Week 4 — Postgres and RDS
## Required Homework:
### Create RDS Postgres Instance:
I've used the CLI to create the RDS Postgres instance as instructed.  
![rds postgres](assests/week04/hwrq-0101-rds.png)
### Bash scripting for common database actions:
I've created all the required scripts in the `backend-flask/bin` directory as follows:
* db-connect
* db-create
* db-drop
* db-schema-load
* db-seed
* db-sessions
* db-setup
* rds-update-sg-rule

Executing the scripts locally
![bash scripts locally](assests/week04/hwrq-0201-scripts.gif)  
Executing the scripts to prod rds
![bash scipts prod](assests/week04/hwrq-0202-scripts-prod.gif)  

### Install Postgres Driver in Backend Application:
I've used the *psycopg* package as instructed.
* Put in `requirements.txt`:
```
psycopg[pool]
psycopg[binary]
```
* Import and use its pool feature inside a class:
```python
# db.py
from psycopg_pool import ConnectionPool
...
class Db:
  def __init__(self):
    self.pool = ConnectionPool(os.getenv("CONNECTION_URL"))
...
```
### Connect Gitpod to RDS Instance:
I was able to connect Gitpod to the RDS intstance using the db-connect script.  
![gitpod to rds](assests/week04/hwrq-0401-connect-rds.png)

### Create Congito Trigger to insert user into database:
I've created the Cognito trigger and the associated lambda function to insert the user into the database.  
Cognito Trigger:  
![Congito Trigger](assests/week04/hwrq-0501-cognito-trigger.png)  
Associated Lambda:
![Lambda](assests/week04/hwrq-0502-cognito-trigger-lambda.png)  
Demo:
![Demo](assests/week04/hwrq-0503-demo.gif) 
### Create new activities with a database insert:
So in order to do that, I needed to pass a valid *user_handle* to the `Db` class to be able to insert the "crud" (activity) without errors. Initially I've receive an error complaining of a null user_uuid. Tracing the issue, I've discovered that the *user_handle* that's passed to `CreateActivity.run` is hardcoded to "andrewbrown" which makes senses to generate an null error as I don't have that user_handle in my *users* table (unless I signup using that handle, which I didn't). So one way I could solve this is to pass the *user_handle* (preferred_username) from the frontend to the backend in a similar way we did for the JWT token. I've modified the *SigninPage.js* page's `onsubmit` function to store the *user_handle* in the browser's localStorage:
```javascript
//SigninPage.js
...
localStorage.setItem("user_handle", user.attributes.preferred_username);
...
```
Then in the *ActivityForm.js*, I'd pass the stored *user_handle* to the backend endpoint (data_activities)
```javascript
//ActivityForm.js
...
const res = await fetch(backend_url, {
...
          user_handle: localStorage.getItem("user_handle")
});
...
```
And finally, modify `data_activities` in *app.py* (/api/activities endpoint) to receive *user_handle* from the received request
```python
def data_activities():
    user_handle = request.json["user_handle"]
    ...
```
This will make sure that the backend will query (and insert) the data for the correct singed in user withou throwing any errors.  
Demo:  
![insert activity](assests/week04/hwrq-0601-insert-activity.gif)  

## Homework Challenges:
### Tweeking the db-setup script:
I've tweeked the *db-setup* script to work with prod rds as I needed a way to reset it, clear all data and possible seeding it for test purposes. The script warns the user if he/she is using it on prod and requires an confirmation. Also, It won't seed the prod db unless the user confirmed.  
![modified db-setup](assests/week04/hwch-0101-db-setup.gif)  
### Creating a test for Lambda:
While developing the AWS lambda, I've found that creating a test will be very useful. First I've executed the function and printed the *event* param. Then I used the same JSON data I've received as the test template.  
