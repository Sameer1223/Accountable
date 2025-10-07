# Accountable
Full stack group habit tracker that you can share with friends to hold each other accountable

Motivation: I wanted to build a project that would mimic the accountability of verbally agreeing on building good habits with friends and family. This project was intended to build habits together as a little mini game keeping the streak up to ensure a healthy and productive lifestyle.

## Project Url
https://accountableweb.netlify.app/

Project Dependencies are in the backend/src/ folder in the requirements.txt file

BUT you can just access the full app hosted on render on the link above. Frontend is hosted on Netlify and backend on Render. Authentication can be done through the login button on arrival to the page. You can use the Auth0 portal to login and then perform tasks.

### Features
Users can: 
- Login through Auth0 authentication
- Create groups and invite members by email
- Create, read, update, and delete habits in a group
- Can mark tasks as complete increasing the streak if everyone has completed the task
- Track their daily progress towards completing their goals alongside their friends
- Switch between their friend groups to access other shared tasks
- Tasks only show on the days they are assigned!

### Tech Stack
- Python and Flask for the backend
- Javascript and React for the frontend

### API
- Two roles: Habit User and Group Admin
- Habit user can do all basic tasks
- Group admin has control on inviting people to the group

Endpoints:
- GET /tasks – Returns a list of all tasks in the database (for testing, requires get:tasks permission).
- GET /tasks/<id> – Retrieves details for a specific task by its ID (for testing).
- GET-  /tasks-today/<user_id> – Returns all tasks scheduled for today for a given user (requires get:tasks-today permission).
- POST /tasks – Creates a new task for a specific user or group (requires post:tasks permission).
- PATCH /update-streaks/<user_id> – Resets streaks and completion states for a user’s past tasks based on last login.
- PATCH /tasks/<id> – Updates a specific task’s details (requires patch:tasks permission).
- DELETE /tasks/<id> – Deletes a task by its ID (requires delete:tasks permission).

- GET /groups – Retrieves and returns a list of all groups (requires get:groups permission).
- GET /groups/<g_id> – Retrieves detailed information about a specific group by its ID (requires get:group-by-id permission).
- POST /groups – Creates a new group with a given name and owner (requires post:groups permission)

- PATCH /users/<user_id>/groups/<group_id> – Adds a user to a specific group and increments that group’s member count (requires patch:add-user-to-group permission).
- DELETE /users/<user_id>/groups/<group_id> – Removes a user from a specific group and decrements that group’s member count (requires delete:user-group permission).

- GET /users/<user_id> – Retrieves a specific user by their Auth0 user ID.
- GET /users-by-email/<email> – Retrieves a user by their email address (used for login/invites).
- POST /users – Adds a new user to the database or returns the existing one if already present.
- PATCH /users/<user_id> – Updates the user’s last checked day (used for tracking daily logins).

### How to run
The project is already hosted ready to use on the link above but if you want to run locally:

Frontend:
 - Go into the frontend folder and perform: npm start

Backend:
- Install requirements from requirements.txt
- Execute the Flask API file by setting env variables and running the file
    export FLASK_APP=api.py
    export FLASK_ENV=development
    flask run
  OR
  python3 api.py
