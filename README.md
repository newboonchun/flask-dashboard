# flask-dashboard
a flask dashboard with chart.js to visualize the data from excel

for the latest commit - render deployment 
- currently using ngrok to deploy the flask app
- render is not appropriate as the excel file need to be at bitbucket (to be updated from time to time)
- so, the requirement.txt file is not usable since render is not use.

for the ngrok, flask app must run first (currently flask is run through wsgi server)
--> python wsgi.py

after that, run ngrok.
-->ngrok.exe http 5000
