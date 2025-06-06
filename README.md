# Repo: python-users-restapi
![Static Badge](https://img.shields.io/badge/Dev_status-Development-green)

## Reason: Python Learning - REST API / Flask

### Description
This is a more robust rest api that I have created using Python and Flask. 
It is based upon my previous Node.JS/Express.JS experience and looks to implement the following:
 

- Server listener
- DB Connection (MongoDB)
- Separated concerns for User:
  - user_model
  - user_routes
- Read environment variables from .Env file

I have currently implemented the following routes:
- GET - all users
- POST - create a new user

my Todo list is:
[] GET - single user by username
[] PUT - update a user
[] DELETE - delete a user
[] Encryption - currently the password is stored as an open string. this needs to be stored as an encrypted string.

### .env File:
PORT=
MONGO_URI=
MONGO_DB=

### Tech Stack/Dependencies:

- Python
- Flask
- pymongo
- pydantic
- typing
- bson
- os
- dotenv
- Insomnia
