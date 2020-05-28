import bonobo
import requests
import csv
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# url = 'https://restcountries.eu/rest/v2/name/united'
url = 'https://restcountries.eu/rest/v2/all'

# remove CSV file if exists.
csv_filepath = 'test.csv'
try:
    os.remove(csv_filepath)
    with open(csv_filepath, 'w', newline='') as new_csv:
        writer = csv.DictWriter(new_csv, fieldnames=["name", "capital", "region", "population", "languages"])
        writer.writeheader()

except:
    print("Error while deleting file ", csv_filepath)

# rds setting
rds_connection_string = "postgres:password@localhost:54320/world"
engine = sqlalchemy.create_engine(f'postgresql://{rds_connection_string}')

Base = automap_base()
Base.prepare(engine, reflect=True)

# drop table and recreate table
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# World ORM class
World = Base.classes.world_table


# Extract data using API
def extract():
    yield from requests.get(url).json()


def transform(data):
    print(data)
    entry = [data['name']]
    # keys = {'name', 'capital'}
    # entry = { k:v for k,v in data.items() if k in keys }
    if data['capital'] is "":
        data['capital'] = 'NA'
    entry.append(data['capital'])
    entry.append(data['region'])
    entry.append(int(data['population']))
    entry.append(data['languages'][0]['name'])
    yield entry


def load_csv(entry):
    print('load --->', entry)
    # with open(fname, 'a+') as f:
    #     f.write(json.dumps(entry) + '\n')
    with open(csv_filepath, 'a') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([*entry])
    yield entry


def load_postgres(entry):
    print('load postgres --->', entry)
    session = Session(engine)
    new_country = World(name=entry[0], capital=entry[1], region=entry[2], population=entry[3], languages=entry[4])
    session.add(new_country)
    session.commit()


def get_graph():
    graph = bonobo.Graph()
    graph.add_chain(extract,
                    transform,
                    load_csv,
                    load_postgres,
                    bonobo.Limit(1000),
                    bonobo.PrettyPrinter())
    return graph


def get_services(**options):
    return {}


if __name__ == '__main__':

    parser = bonobo.get_argument_parser()

    with bonobo.parse_args(parser):
        bonobo.run(get_graph())
