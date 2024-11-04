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

#### Frontend Elements
- Progress bar
- Drop down categories
- Tasks (like to do lists)
- Task add/edit page
- Group add/invite page
- Login page

#### Additional Considerations
- Interactions with groups mainly:
  - Should have an invite that needs to be accepted rather than the ability to add anyone
  - 
 
