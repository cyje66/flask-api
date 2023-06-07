# flask-api
A practice using flask to write two RESTful APIs: /register and /login. Keywords: flask, sqlite, docker

## Steps: 
1. `docker pull eddiechien/flask-api:latest`
2. `docker run -p 5000:5000 eddiechien/flask-api`
3. open API tester, type GET http://localhost:5000/account, start testing

## API Doc
| Method | Route | Description | Request body | Response description |
| ------ | ----- | ----------- | ---------- | ---------------------- |
| GET    | /account | Get all accounts | None | {<br>  &emsp;"users": list of users <br>} |
| POST   | /register | Create an account | username <br> password | {<br> &emsp; "success": true or false, <br>&emsp; "reason": reason <br>} |
| POST   | /login    | Verify an account | username <br> password | {<br> &emsp; "success": true or false, <br>&emsp; "reason": reason <br>} |

#### Rules
* Length of username should be no less than 3 characters and no longer than 32 characters.
* Length of password should be no less than 8 characters and no longer than 32 characters.
* Password should contain at least 1 number, 1 lowercase and 1 uppercase letter.
* Cannot register account if an username is under registration.
