# Globant Challenge

Welcome to **Globant’s Data Engineering** coding challenge.

In the context of a DB migration with 3 different tables:
- departments
- jobs
- employees

**Create a local REST API that must:**
1. Receive historical data from CSV files.
2. Upload these files to the new DB.
3. Beable to insert batch transactions (1 up to 1000 rows) with one request.

You need to explore the data that was inserted in the previous section. The stakeholders ask for some specific metrics they need. You should create an end-point for each requirement.

**Requirements:**
1. Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.
2. List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending)

**Chosen Stack**
To tackle this project, I've chosen the following technologies: FastAPI (Python) for backend development and PostgreSQL as database management system. The selection of these technologies is based on their versatility, efficiency, and ability to provide a scalable solution quickly and effectively.

**Repository**
In this repository you have two main folders:
- backend
- container

**backend**: contains all the source code and configurations needed to execute the application on your local system. 
**container**: containerized all the source code and docker files to deploy containers and be able to run the application with  a simply ```docker compose up --build```


#### Next Steps
Developt a frontend to allow stakeholders use the application in a more friendly way. 

Once you have started the local server, open your web browser and navigate to: 

> http://localhost:8000/docs


How to make the app run? Follow the steps for each case: backend / container.