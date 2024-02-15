# CAPSTONE - BookYourFood

This is my Final Project for the course CS50’s Web Programming with Python and JavaScript. It is built with Django, Hmtl, Css, Javascript, Python & Bootsrap

## Description

Build an app that lets you book where you want to eat today! This app will let you log in and choose from a series of previously added restaurants and let you make a booking for the place you want to reserve.
When the reservation is done it will send the user an email with the reservation info for the booking. The user will also have access to the current reservation it holds and the history of reservations made.

## Distinctiveness and Complexity

I believe my project is distant enough from the projects done in this course since it handles email interaction with the users and manages dates, times, and timezone awareness logic which wasn't used in the previous projects for the course.

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
  - reservation.js: The JS code for fetching and structuring the reservations information
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
- login, logout, and register: User authentiication

## Installation and Running
This project doesn't need any additional dependencies.
You only need to install Django and run the following commands:
```
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver
```
