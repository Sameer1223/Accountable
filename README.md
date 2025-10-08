# Accountable
Full stack group habit tracker that you can share with friends to hold each other accountable

Motivation: I wanted to build a project that would mimic the accountability of verbally agreeing on building good habits with friends and family. This project was intended to build habits together as a little mini game keeping the streak up to ensure a healthy and productive lifestyle.

## Project Urls
### Frontend URL
This works with the backend and all endpoints are connected!

https://accountableweb.netlify.app/

### Backend  URL
Requests are made to this URL and from the frontend application

https://accountable-fzw9.onrender.com


Project Dependencies are in the backend/src/ folder in the requirements.txt file
For env variables run:
>source authVariables.sh

BUT you can just access the full app hosted on render on the link above. Frontend is hosted on Netlify and backend on Render. Authentication can be done through the login button on arrival to the page. You can use the Auth0 portal to login and then perform tasks.

## Authentication Setup and Instructions

You can login through the app and interact with it normally since the frontend and backend are connected and work on the frontend link.

If you want to test the backend, endpoints manually here is how you can get the Auth Token.

1) Open the app frontend @ https://accountableweb.netlify.app/.

2) Click Login and sign up

3) Access the network tab in the devtools and click on any request and access the Authorization Bearer JWT token from the headers.

Then if you want to use the token to manually test endpoints:

- Add a header key value pair
> Authorization: Bearer {your token here}

## Features
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
  - Permissions: 
  ```delete:tasks, delete:user-group, get:group-by-id, get:tasks-today, patch:add-user-to-group, patch:tasks, post:groups, post:tasks```

- Group admin can do all things that a basic habit user can with the added permission of ```get:users```
  - A group admin can use the ```GET /users``` endpoint
  - Permissions:
  ```get:users, delete:tasks, delete:user-group, get:group-by-id, get:groups, get:tasks, get:tasks-today, patch:add-user-to-group, patch:tasks, post:groups, post:tasks```

NOTE:
To test group admin endpoint you can use this provided token:
> eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhTWmNfeUxfS2NNd3BvNXRrQ1pTUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1zMjY2YnJkY20wbTZ6bXQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGU1Y2Q4MTg0OTA4YmRkZDM2YTRlNmUiLCJhdWQiOlsiYWNjb3VudGFibGUiLCJodHRwczovL2Rldi1zMjY2YnJkY20wbTZ6bXQxLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3NTk4OTA5OTIsImV4cCI6MTc1OTk3NzM5Miwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF6cCI6ImdjRTNXY3NPTUdkNHJ3OGlWR3BjaXFhdk9ZQnN3enlGIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnRhc2tzIiwiZGVsZXRlOnVzZXItZ3JvdXAiLCJnZXQ6Z3JvdXAtYnktaWQiLCJnZXQ6dGFza3MtdG9kYXkiLCJwYXRjaDphZGQtdXNlci10by1ncm91cCIsInBhdGNoOnRhc2tzIiwicG9zdDpncm91cHMiLCJwb3N0OnRhc2tzIl19.LVmwwiIT-X7f5zcLHHoM7bLQmOnTyYPDuQZ1Wr7GGz68ZIli9i8L42K2XRJsH07FInn43MYbaM6FMJzjy3qvJ3Ee9PeEPjeqBfz_15Re-pzDPtZfibIvcuJG51oy_eR_8VZ0niZYFZyQP9Aj-HJEgsa4q0a2j94yYlJ2dRGva7govf_tf9GU8Z2ym3xuBIdDisySmUR_Kfvc9_4ob9d8yyUjN4So7SZLDcb_DDWyWmaNIlK9fKFsHbcCu9bGqZ6TZ8f4G_o7BCt-kbHJa5wDaslzfJMnxjLHxRLHPN8m30MrzSP9GXxQOAykJEH-wEzkppqpZNoKsgiPkeY4OBwglQ

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
