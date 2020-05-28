CREATE TABLE world_table (
  id serial PRIMARY KEY,
  name varchar,
  countrycode varchar(5),
  capital varchar(30),
  region varchar(30),
  subregion varchar(30),
  population integer,
  languages varchar(30),
  flag varchar(100)
);

