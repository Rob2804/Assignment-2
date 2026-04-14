Skill Swap Hub – COM4113 Tech Stack

Student Name: Robert Ursache
Student ID: 2407581

### Introduction

This project is based on my first assessment where I created a front-end website for a Skill Swap Hub. In this assignment I developed it further by adding a backend using Flask and connecting it to a MongoDB database so the website fully works.

The main idea of the project is to allow users to share skills and resources with other people. Users can create an account, log in, edit their profile and post resources. Other users can then view these resources, search them or filter by category.

I wanted to turn my static website into something more realistic and interactive, which is why I used a database and backend logic.

### Technology stack

I used Flask for the backend because it is simple and easier to understand compared to other frameworks. Since this is my first time doing backend development, Flask helped me focus on learning the basics without too much complexity.

For the database I used MongoDB Atlas. I chose MongoDB because it is flexible and does not require strict tables like SQL. It was easier for me to store user data and resources as documents.

The frontend is still based on HTML, CSS and Bootstrap from my first assignment, but now it is connected to Flask using templates.

### Installation and Setup

To run the project, the user needs to install Python and then install the required libraries using pip such as Flask, PyMongo and Werkzeug. After that, a MongoDB Atlas cluster must be created and the connection string needs to be added into the app.py file
FOR TESTING PURPOSES, THE MONGODB STRING IS INCLUDED IN THIS PROJECT. THIS INCLUDES MY USER AND PASSWORD. IN A REAL WORLD SCENARIO, THIS SHOULD BE STORED SECURELY!!!

Once everything is set up, the application can be run by double clicking the app.py / alternatively - right click, open with, python ( in case an editor like vs code pops up)

Then it can be accessed in the browser using localhost.

### Database design

The database has two main collections which are users and resources.

The users collection stores information such as username, email, password, bio, hobbies, profile photo and the date the account was created.

The resources collection stores the title, link, description, category, author, author photo, date created and number of likes.

I used MongoDB because it allows storing this kind of data easily without needing a fixed structure.

### Features

The application includes several features. Users can register and log in securely. Passwords are hashed using Werkzeug so they are not stored in plain text. Users can also edit their profile and upload a profile photo.

Another main feature is posting resources. Users can add a title, description, link and category. These are then stored in the database and displayed on the timeline.

The timeline page allows users to search using keywords and filter by category. I have used  MongoDB queries for this.

I also added a like system where users can click a button to increase the number of likes on a resource.

### Risk assesment

There are some risks in this project. One risk is the database connection failing. I handled this by using try and except blocks so the application does not crash completely.

Another risk is users entering invalid data. To reduce this, I added server-side validation to check if fields are empty or incorrect before saving them.

There is also a risk with file uploads. To reduce this, I only allow certain file types such as png and jpg.

### Legal and Ethical consideration

There are also legal and ethical considerations. The application stores user data such as email and profile information. Because of this, GDPR rules should be considered in a real system. Users should have control over their data and know how it is used.

Passwords are hashed which improves security, but in a real application more security features would be needed.

Another issue is that users can post links, so there is a risk of harmful content. This would require moderation in a real system.

### Flask vs Django

When comparing Flask to other frameworks like Django, Flask is much simpler and easier to use. Django has more built-in features but it is more complex and harder to learn.

For this project, Flask was a better choice because it allowed me to focus on understanding backend logic step by step.

### Software Design

In terms of software design, I tried to separate different parts of the application in order to keep it clear and structured. The HTML templates are separate from the Python code, and the database logic is handled inside the Flask routes. This also makes the code easier to read and manage.

### Reflection

One of the biggest challenges was connecting Flask to MongoDB Atlas. At first I had issues with the connection string and database access, but I managed to fix it by checking the configuration.

Another challenge was changing my static HTML pages into dynamic templates using Jinja. It took me a while  to understand how to pass data from Flask to the templates.

Overall, this project helped me understand how a full stack application works and how the frontend and backend connect together.

### Diagram

The database design is quite simple. One user can create multiple resources, which means there is a one-to-many relationship between users and resources.

I included a diagram in the submission zip file, to show the relationship between users and resources

### Github 

GitHub Repository:  
https://github.com/Rob2804/Assignment-2

Due to having an extension, I used a personal repository instead of the classroom repository as it didn't let me use it.

### References



Flask (2024) Flask Documentation. Available at: https://flask.palletsprojects.com/

MongoDB (2024) MongoDB Documentation. Available at: https://www.mongodb.com/docs/

PyMongo (2024) PyMongo Documentation. Available at: https://pymongo.readthedocs.io/

Werkzeug (2024) Password Hashing. Available at: https://werkzeug.palletsprojects.com/

Bootstrap (2024) Bootstrap Documentation. Available at: https://getbootstrap.com/

Mozilla (2024) MDN Web Docs. Available at: https://developer.mozilla.org/

ICO (2023) Guide to GDPR. Available at: https://ico.org.uk/

W3C (2023) Web Accessibility Guidelines. Available at: https://www.w3.org/WAI/standards-guidelines/wcag/

GeeksforGeeks (2024) Flask Tutorial. Available at: https://www.geeksforgeeks.org/python/flask-tutorial/

# USE OF GENERATIVE AI

This assignment used generative AI in the following ways: brainstorming and reviewing code.