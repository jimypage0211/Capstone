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

**AllRestaurants Page:** This is where the user goes when it's logged in. This page will show you the list of all possible restaurants to book. Each restaurant has a link to reserve the table(s) you need for your diners. If the user is not logged in, once it clicks a reserve link, the app will redirect the user to the log-in page.

**Reserve Page:** On this page the user will select the number of diners and the time of the reservation. The user will get a series of alerts depending on if the information on the reservation is correct. For example, if the user selects a time for which the restaurant is closed, it will get an alert.

**Reservations Page:** This is where the user can check their active or past reservations. Here the user can also cancel an ongoing reservation or unarchive a past reservation.

### Files
This project contains the structure of a default Django app. In addition, it contains the following folders:
- **Static folder:** This contains a folder called reservations that contains:
- allRestaurants.js: The JS code for fetching and structuring the restaurant information
- reservation.js: The JS code for fetching and structuring the reservations information
- styles.css: In addition to bootstraps, this contains some styling code for the whole app


