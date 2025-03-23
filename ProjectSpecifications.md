### Models
 - **Tasks**: Attributes include name, status, frequency, days, streaks, shared, and group id?
 - **Group**: Attributes include group id, members, shared tasks?
 - **Users**: Attributes include user id, name, badges, etc

 ### Endpoints
 - **GET** /tasks/today and /tasks/all /group
 - **DELETE** /tasks/{id}
 - **POST** /tasks and /group
 - **PATCH** /tasks/{id}

 ### Roles
  - **Regular**: Interacts with only their own tasks
  - **Group Admin**: Can add members and create shared tasks

#### Features
- Habit tracker checklist
- Categories of tasks
- Progress bar to show completion
- Streaks to count frequency of habit
- Tasks showing only on their scheduled time frames
- Shared tasks in groups where everyone progresses the tasks
- Or just a shared task not visible to a group but select members (difference being group is all shared vs sharing one task does not require creation of a group)

#### Frontend Elements
- Progress bar
- Drop down categories
- Tasks (like to do lists)
- Task add/edit page
- Login page
- Group add/invite page

#### Additional Considerations
- I should cut the groups part for now and focus on shared tasks
- Interactions with groups mainly:
  - Should have an invite that needs to be accepted rather than the ability to add anyone
  - Should ideally locally store private tasks
  - Initially should just be groups have tasks, then expand to private tasks
  - Task should have the capability to count how many people of the assigned persons completed the task, all persons completing the tasks furthers the goal
 
#### To Do:
1. Don't refresh the completed checkmark
2. Have it so checkmark can be unselected for now
3. Progress component
4. Progress bar
5. ~~Categories based on daily, weekly, important? Might not be needed because tasks only show on days~~
6. Edit option for tasks
7. Reset streaks if missed -> last checked, then for all past days missed reset tasks to incomplete and set streaks to 0 if not completed
8. Individual and Group tab section
9. CRUD for groups
10. User login page
11. User authentication
12. User auth

### Updated To Do:
1. CSS Styling
2. Users should be able to accept or decline group invites
3. Group admin should be able to manage members
4. Clicking on a task should expand stats and reveal member completion stats
5. Right clicking a task should allow for popup to edit and delete
6. User experience upgrades
