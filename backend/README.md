# Globant Challenge

Source code and config specifications of the aplication.
I developed this solution on Ubuntu 22.04.4 LTS Virtual Machine.


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
    name VARCHAR(255) NULL,
    datetime TIMESTAMP WITHOUT TIME ZONE NULL,
    department_id INTEGER,
    job_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE SET NULL
);
```

Let’s create a new user for security reasons:

```
create user apl_apimigration with password 'xxxxxx';
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

Now, let's activate python virtual env and install dependencies:

```
source env/bin/activate
pip install -r requirements.txt
```

With everything installed. Execute the following command to start the console: 

> uvicorn main:app