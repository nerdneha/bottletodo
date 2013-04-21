bottletodo
==========

This was my second web app (that wasn't a "hello world") and my first app where I explored using a database and interactions between pages. I learned the difference between a GET and POST on this and explored authentication with this site for the first time. 

I used: Python 2.7.3, the Bottle Framework, and MongoDB. To use my tech, go to
    requirements.txt

####To start the app:
    python sign-up.py

The app has you sign up for an account or log in to an existing account (Hacker Schoolers can go directly to the log in page because I use their auth). From there you will see todo list items (known as tasks) split by open tasks and closed tasks. You can:
* Add a task
* Edit a task name/status
* Open/Close a task
* Logout

Users can opt to log in as "anonymous" which lets you view the site but prevents you from adding or editing tasks. Cookies are used to store your session and are removed upon logout. 

