# Racemate - running app

## Technology Stack:

Frontend: Bootstrap  
Backend: Django, Python, Django Rest Framework  
Database: PostgreSQL  

## Functionality:  

### For anonymous user:  
Register - User enters his or her name, email, password and password confirmation  

Login - Email and password  

Running Calculator - calculate VDOT(runner's efficiency), training tempos and competition results  

About  
Contact  

### Only for logged user:  
Main Page - Main Page is splited in two columns. Right shows user's VDOT(runner's efficiency) and last trainings. Left is for user's personal records and his groups.  

Edit Profile - User can add some information about him or her, only username is required. User can't access the rest of the application without created profile.  

Add trainig - Form for adding new past training, user can also automatically calculate VDOT from training's results  

Training plans  - long-term training plans (actually - 16-weeks plan for beginers and last 18-weeks plan to marathon). Running tempos are calucalated from VDOT(runner's efficiency)  

Your running groups - shows all groups in which user is a member and all of those groups' members(with last login, date of joining and efficiency)  

Create running group - form to create runnung group - user became a admin  

Joing the runing group - shows all groups user can join with join button.  

Messages - massages view is splited in two columns. Right shows all of user's group and left all of his 'friends'(members of his/her groups). From this view user can goes to sending message form.  

API - available for logged used. Contains users, groups and user's past trainings  

https://racemate-app.herokuapp.com/  


