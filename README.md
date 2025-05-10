# studybuddy

Project Title: StudyBuddy

Team Members:
- Smithi Mahendran
- Manasa Vinod Kumar
- Neel Mokaria
- Karan Agarwal


Overview:
StudyBuddy is a collaborative web application built with Flask that helps students enhance their learning experience by forming study groups, scheduling sessions, sharing materials, and taking topic-based quizzes. It encourages collaborative learning through real-time interaction and knowledge checks.

Registration and Login:

- Register: Users provide a username, email, and password to create an account
- Login: Authenticates existing users with email and password
- Logout: Ends the current user session securely

Forms:

- Register Form
  Fields – username, email, password

- Login Form
  Fields – username, password

- Create Study Group Form
  Fields – course name, description, tags

- Session Scheduler Form
  Fields – date/time, Zoom link, group name

- Trivia Quiz Form
  Fields – topic selection, number of questions, difficulty

Blueprints:

- Auth
  /register – Create a new user
  /login – Log in to an existing account
  /logout – Log out from the current session

- Study
  /create-group – Create a new study group
  /group/<id> – View group details, sessions, and resources
  /schedule-session – Set up collaborative study sessions
  /upload-resource – Upload or link to study materials
  /quiz – Generate and take quizzes by topic

Features for Logged-In Users:

- Create and join study groups
- Schedule and join study sessions (e.g., via Zoom)
- Upload, view, and download study resources
- Comment on sessions and resources
- Take quizzes on chosen topics

Database:

We used MongoDB via PyMongo to store:

- users – User credentials and profiles
- groups – Study group metadata (name, tags, etc.)
- sessions – Scheduled session information
- resources – Files and links shared in study groups
- comments – Comments on resources and sessions
- quizzes – Quiz attempts to test user knowledge

Database Operations:

- Creating a group → inserts into groups
- Scheduling a session → inserts into sessions
- Uploading a resource → inserts into resources
- Posting a comment → inserts into comments
- Taking a quiz → fetches from API

API:

Trivia API
Used to dynamically generate quizzes by:
- Fetching multiple-choice/true-false questions based on topics, difficulty, and number of questions
