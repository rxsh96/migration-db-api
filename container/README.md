# Globant Challenge

Source code and config specifications of the containerized application in Docker.

# Requirements
- Docker version 25.0.3
- Docker Compose version v2.24.6
 
**Deployment**
With docker and docker compose installed on your computer, simply execute the following command:
```
docker compose up --build
```

**Explanation**
Considering the following tree: 
```
├── backend
│   ├── app
│   │   └── api
│   │       ├── database
│   │       ├── endpoints
│   │       └── models
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── database
│   └── init.sql
├── docker-compose.yml
└── README.md
```

In docker-compose.yml I specified the images for both Fast API Python Backend and PostgreSQL Database. 

This yml file points ./app/Dockerfile in fastapi-app section to create the image with all python dependencies from requirements.txt.  

Also, the yml file, postgres-db section, I specified a volume with the initial init.sql file to create the tables and connection user. 