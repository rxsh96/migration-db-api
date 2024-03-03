# Globant Challenge

Welcome to **Globant’s Data Engineering** coding challenge.

# Section 1: API

In the context of a DB migration with 3 different tables:

- departments
- jobs
- employees

Create a local REST API that must:

1. Receive historical data from CSV files.
2. Upload these files to the new DB.
3. Beable to insert batch transactions (1 up to 1000 rows) with one request.

To tackle this project, I've chosen the following technologies: FastAPI (Python) for backend development, React (JavaScript) for frontend design, and PostgreSQL as the database management system. The selection of these technologies is based on their versatility, efficiency, and ability to provide a scalable solution quickly and effectively.

# Requirements

**1. Instalation of PostgreSQL in Ubuntu 22.04.4 LTS**
You can refer to the official docs: [PostgreSQL: Linux downloads (Ubuntu)](https://www.postgresql.org/download/linux/ubuntu/)

Run the following commands on Terminal:

```
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```

**2. Configuring a PostgreSQL Database**

```
sudo -i -u postgres
psql
```

Let's change the postgres user password:

```
\password postgres
```

Let’s create our challenge database and connect to it:

```
create database migrationdb;
\c migrationdb
```

Now, we can create the tables from the CSV file’s structure:

```
CREATE TABLE departments (
	id SERIAL PRIMARY KEY,
	department VARCHAR(255) NOT NULL
);

CREATE TABLE jobs (
	id SERIAL PRIMARY KEY,
	job VARCHAR(255) NOT NULL
);

CREATE TABLE hired_employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
	datetime TIMESTAMP NOT NULL,
	department_id INTEGER NOT NULL,
	job_id INTEGER NOT NULL,
	CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id),
	CONSTRAINT fk_job FOREIGN KEY (job_id) REFERENCES jobs(id)
);
```

Let’s create a new user for security reasons:

```
create user apl_apimigration with password 'apl123UseR';
```

Grant to apl_apimigration read and write access to public sheme, commit changes and exit.

```
grant connect on database migrationdb to apl_apimigration;
grant select, insert on all tables in schema public to apl_apimigration;
commit;
\q
```

### Optional:

To enable remote access to PostgreSQL Server, add the following:

```
cd /etc/postgresql/<version>/main/
sudo vi postgresql.conf
```

Find the line: #listen_addresses = 'localhost'. Uncomment it and change the value to:

> listen_addresses = '\*'

Save changes.

```
sudo vi pg_hba.con
```

At the end of the file, add the following line:

> host all all 0.0.0.0/0 md5

Save changes.
Now, we can connect to our PostgreSQL Database.

**3. Create Virtual Environment for Python**

I've created a virtual environment called "env" inside backend directory

```
python3 -m venv env
```

    migration-db-api
    ├── backend
    │   └── env
    └── README.md

Now, let's activate python virtual env and install fastapi library

```
source env/bin/activate
pip install "fastapi[all]"
pip install SQLAlchemy
```

With fastapi installed, let's start coding!