# Description
This is the project I worked on at my Internship at datamachines.co over the 2021 summer

The project is for creating a stacking bar graph with the help of the d3 utilities to visualize login data during a specified period. This is to help administrators quickly understand how often and which users are using a certain service at a glance. The initial raw data will be collected from an automated Nginx service that will pull the log files. Cronjob will be used to automate refreshing the service to include new data.

The objective of this project was to take the login data of our services and visualize with a graph how often our products were used based on how many times users logged into the application. Python will be used to analyze and format the data from the log files into a CSV format. With the new data, the program will display the data in a chart by using d3 through the index.html file. 

The main repository for this project is stored in GitLab, where CI/CD has been set up to automatically build and test a working docker image to be used. 

The entire project has been dockerized and has an ansible-playbook setup to allow a user to deploy this service to any machine.

##Requirements
1. Download the docker-compose.yml file from the repository. 
2. The Nginx service set up to collect logs for user logins must already be set up and stores the logs in the "nginx" directory
3. The docker-compose.yml, "data" directory, and "nginx" directory must all be all placed in the same directory.

  - Create the "data" directory if one does not already exist. 
  - The "nginx" directory is where the login data logs are stored by the service that automatically collects it. 

##Useage:
docker-compose up

##Recommendations 
Once the service is up and running, set up a cronjob to execute refresh the chart to account daily to account for new data.

##Overview

###data
This is a directory that is used to volume mounts data used in the project through in the docker-compose file

###nginx
The directory that the Nginx service stores the logs of login information and app usage of users in the company.

###AccessLog.py
This code does the following
  1. Parse through the logs in Nginx and generate an "app.qcr.io.access.log" file
  2. Analyzes and formats the data from "app.qcr.io.access.log" as well as generate a CSV file with the data stored at ./static/js directory
  3. Uses flask to render the "index.html" file and host it in localhost.
