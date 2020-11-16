# FlaskWithWebsockets

This project is an exercise in implementing a Flask web server that will act as an
intermediary between two clients. All communication between the server and the clients
will be using web sockets. A large part of the code implemented on the server is derived 
from Miguel Grinberg: https://blog.miguelgrinberg.com/index and all of his amazing tutorials.

## Instructions:

Server:
1. Download all files in repository and place them in a folder on your computer.

2. Using Command Line / Command Prompt / PowerShell navigate to the folder with all of the files.

3. You'll need to create a virtual enviornment to host the Flask server.
    - Instructions can be found here: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    
4. The server also uses a database to store user information
    - Instructions for intitalizing the database can be found here: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
    
5. Once virtual environment has been created and database has been initialized inside of it, you can start up the flask server with the following command.
    - flask run
    
Web Client:
1. While an instance of the server is running navigate to the web page: http://127.0.0.1:5000

2. If you do not have an account registered on your server create one, if you do log in.
    - python client only currently works for username: luke mcdaniel

3. After logging in you will be redirected to the main page of the website where you can send messages to other clients.

Python Client:
1. The file client.py contains the code for the server independant client.

2. Run this file with the following command.
    - python client.py
    
3. For this client to work, an instance of the server must be running and, user with username luke mcdaniel must be logged into the server.
