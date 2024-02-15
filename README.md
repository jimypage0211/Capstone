# CAPSTONE - BookYourFood

This is my Final Project for the course CS50’s Web Programming with Python and JavaScript. It is built with Django, Hmtl, Css, Javascript, Python & Bootsrap

## Description

Build an app that allows you to book your preferred dining spots! This app enables users to log in, choose from a list of previously added restaurants, and make reservations at their desired locations.
Upon completing a reservation, the app will send an email to the user with the booking details. Users will have access to their current reservations as well as a history of their past bookings.

## Distinctiveness and Complexity

I believe my project distinctly differs from others in this course by incorporating email interactions with users and managing date, time, and timezone awareness, functionalities not covered in previous course projects.

## Structure
### Pages  
**Log-In and Register Pages:** This is where the user can log in or register as a new user.

**Index Page:** This is where the user goes when it's logged in. This page will show you the list of all possible restaurants to book. Each restaurant has a link to reserve the table(s) you need for your diners. If the user is not logged in, once it clicks a reserve link, the app will redirect the user to the log-in page.

**Reserve Page:** On this page the user will select the number of diners and the time of the reservation. The user will get a series of alerts depending on if the information on the reservation is correct. For example, if the user selects a time for which the restaurant is closed, it will get an alert.

**Reservations Page:** This is where the user can check their active or past reservations. Here the user can also cancel an ongoing reservation or unarchive a past reservation.

#### All Pages extend from a layout.html that contains a nav bar to navigate through the app

### Files
This project has the structure of a default Django app. In addition, it contains the following folders:
* **Static folder:** This contains a folder called reservations that contains:
  - allRestaurants.js: The JS code for fetching and structuring the restaurant information
  - reservation.js: The JS code for fetching and structuring the reservation information
  - styles.css: In addition to bootstraps, this contains some styling code for the whole app

* **Templates:** This contains a folder called reservations that contain the templates for the pages mentioned in the Pages section

### Views
This app is made with a blend of Django views and Vanilla JS. The Django views I used are:
- index: It renders the main page of the app (core functionality in JS)
- reservations: It renders the reservations pages (core functionality in JS)
- reserve: It renders the reserve page. It also handles the functionality of the page using Python and Django.
- getReservations: This view finds all the reservations for the current user and returns them to the page via JSON
- getAllRestaurants: This view finds all the restaurants and returns them to the page via JSON
- cancel: This view is for canceling the reservation
- archive: This view is for unarchiving a past reservation
- login, logout, and register: User authentication

## Installation and Running
This project doesn't need any additional dependencies.
You only need to install Django and run the following commands:
```
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver
```
## Notes
This app sends confirmation emails after a reservation is made. The confirmation emails come from the Gmail address "jimyprestaurants@gmail.com".
This email account is used for the sole educational purpose of handling reservation confirmations and nothing more. To connect to the Gmail servers an app authentication password is required and is set up in the settings.py file of the project.

# Thanks for providing these awesome courses!!!


