# flask-api
A practice using flask to write two RESTful APIs: `/register` and `/login`. Keywords: flask, sqlite, docker

## Steps: 
1. `docker pull eddiechien/flask-api:latest`
2. `docker run -p 5000:5000 eddiechien/flask-api`
3. open API tester, type GET http://localhost:5000/account, start testing

## API Doc
| Method | Route | Description | Request body | Authorization | Response description |
| ------ | ----- | :-----------: | :----------: | :---------------: | ---------------------- |
| GET    | /account | Get all accounts | None | No | {<br>  &emsp;"users": list of users <br>} |
| POST   | /register | Create an account | username <br> password | No | {<br> &emsp; "success": true or false, <br>&emsp; "reason": reason <br>} |
| POST   | /login    | Verify an account | username <br> password | Yes <br> Use basic auth | {<br> &emsp; "success": true or false, <br>&emsp; "reason": reason <br>} |

#### Rules
* Length of username should be no less than 3 characters and no longer than 32 characters.
* Length of password should be no less than 8 characters and no longer than 32 characters.
* Password should contain at least 1 number, 1 lowercase and 1 uppercase letter.
* Cannot register account if an username is under registration.

#### Examples
| Method | Route | Request body | Response |
| ------ | ----- | ---------- | ------- |
| GET    | http://localhost:5000/account  | None | {<br>  &emsp;"users": [] <br>} |
| POST   | http://localhost:5000/register | { <br>&emsp; "username": test <br>&emsp; "password": "Aa12345678" <br>} | {<br> &emsp; "success": true, <br>&emsp; "reason": "Account Created." <br>} |
| POST   | http://localhost:5000/login    | {<br>&emsp; "username": test <br>&emsp; "password": "Aa12345678" <br>} | {<br> &emsp; "success": true, <br>&emsp; "reason": "Login successful." <br>} |
