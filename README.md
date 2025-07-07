# Accountable
Full stack group habit tracker that you can share with friends to hold each other accountable

### Features
Users can: 
- Login through Auth0 authentication
- Create groups and invite members
- Create, read, update, and delete habits in a group
- Can mark tasks as complete increasing the streak if everyone has completed the task
- Track their daily progress towards completing their goals alongside their friends
- Switch between their friend groups to access other shared tasks
- Tasks only show on the days they are assigned

### Tech Stack
- Python and Flask for the backend
- Javascript and React for the frontend

### How to run
Frontend:
 - Go into the frontend folder and perform: npm start

Backend:
- Execute the Flask API file by setting env variables and running the file
    export FLASK_APP=api.py
    export FLASK_ENV=development
    flask run
  OR
  python3 api.py
