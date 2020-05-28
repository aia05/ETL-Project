# ETL-Project

## Bonobo ETL

#### Bonobo is a lightweight Extract-Transform-Load (ETL) framework for Python 3.5+.

- Extract data from https://restcountries.eu/ API
- Transform data. Select and convert data from JSON format into columnar data for SQL database
- Load data into CSV file and PostgreSQL database

![alt text](./bonobo-etl/app.png 'ETl flow')

#### Instruction

- Create table in PostgreSQL using 'schema.sql'
- Run docker-compose to start PostgreSQL

```sh
$ docker-compose up -d
```

- Run Bonobo ETL

```sh
$ bonobo run app.py
```

- It will generate CSV file and also load data into PostgreSQL.
