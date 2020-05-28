import bonobo
import requests
import csv
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

url = 'https://restcountries.eu/rest/v2/all'

csv_filepath = './loaded_data/world.csv'

try:
    # remove CSV file if exists.
    os.remove(csv_filepath)
    with open(csv_filepath, 'w', newline='') as new_csv:
        writer = csv.DictWriter(new_csv,
                                fieldnames=[
                                    "name", "capital", "region", "countrycode",
                                    "capital", "region", "subregion",
                                    "population", "languages", "flag"
                                ])
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
    entry = [data['name']]
    entry.append(data['alpha3Code'])
    if data['capital'] is "":
        data['capital'] = 'NA'
    entry.append(data['capital'])
    entry.append(data['region'])
    entry.append(data['subregion'])
    entry.append(int(data['population']))
    entry.append(data['languages'][0]['name'])
    entry.append(data['flag'])
    yield entry


def load_csv(entry):
    with open(csv_filepath, 'a') as f:
        csv_writer = csv.writer(f,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([*entry])
    yield entry


def load_postgres(entry):
    session = Session(engine)
    new_country = World(name=entry[0],
                        countrycode=entry[1],
                        capital=entry[2],
                        region=entry[3],
                        subregion=entry[4],
                        population=entry[5],
                        languages=entry[6],
                        flag=entry[7])
    session.add(new_country)
    session.commit()


def get_graph():
    graph = bonobo.Graph()
    graph.add_chain(extract, transform, load_csv, load_postgres,
                    bonobo.Limit(1000), bonobo.PrettyPrinter())
    return graph


def get_services(**options):
    return {}


if __name__ == '__main__':

    parser = bonobo.get_argument_parser()

    with bonobo.parse_args(parser):
        bonobo.run(get_graph())
