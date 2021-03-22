import csv
from datetime import datetime
from os import path
import requests
from sodapy import Socrata

APP_TOKEN = 'wHvXxdmw8Ek59fQThcHly6ulQ'
DATASET_IDENTIFIER = '5uug-f49n'
CLIENT = Socrata("data.cityofnewyork.us", APP_TOKEN, timeout=30)

def pull_new_data(
    client,
    dataset_id,
    output="../../data/raw/raw_data",
    query="sample_date > '1979-12-31T00:00:00.000'",
):

    date = datetime.now().strftime("_%Y_%m_%d.csv")
    output = output + date

    if path.exists(output):
        return "Data has alread been pulled today. Try again tomorrow."

    with open(output, "w", newline="") as f:
        for page in client.get_all(
            dataset_id, content_type='csv',
            where=query,
            limit=1000):

            writer = csv.writer(f)
            writer.writerows([page])
