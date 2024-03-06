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

create user apl_apimigration with password 'apl123UseR';

grant connect on database migrationdb to apl_apimigration;
grant select, insert on all tables in schema public to apl_apimigration;
commit;