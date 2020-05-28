CREATE TABLE world_table (
  id serial PRIMARY KEY,
  country varchar,
  country_code varchar,
  capital varchar,
  region varchar,
  subregion varchar,
  population integer,
  flag varchar,
  native_name varchar
);

CREATE TABLE gdp (
  id serial PRIMARY KEY,
  country varchar,
  gdp,
  country_code varchar
);

