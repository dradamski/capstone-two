import csv
from datetime import datetime
from glob import glob
import os
import pandas as pd
import re
import requests
from sodapy import Socrata

APP_TOKEN = 'wHvXxdmw8Ek59fQThcHly6ulQ'
DATASET_IDENTIFIER = '5uug-f49n'
CLIENT = Socrata("data.cityofnewyork.us", APP_TOKEN, timeout=30)

def pull_new_data(
    client,
    dataset_id,
    output="../data/raw/raw_data",
    query="sample_date > '1979-12-31T00:00:00.000'",
    limit=100000
):
    """
    Checks to see if a raw file exists and pulls new data to add to it.

    client :
    """

    for filename in  glob(f"{output}*.csv"):
        with open(filename) as f:
            last_line = f.readlines()[-1]
            max_date = re.search(
                "([0-9]){4}-([0-9]).*", last_line
            )[0].split(",")[0]
        query = f"sample_date > '{max_date}'"

    date = datetime.now().strftime("_%Y_%m.csv")
    output = output + date

    if os.path.exists(output):
        return "Data has alread been pulled this month. Try again later."

    with open(output, "w", newline="") as f:
        for page in client.get_all(
            dataset_id, content_type='csv',
            where=query,
            limit=limit):

            writer = csv.writer(f)
            writer.writerows([page])

def combine_old_and_new_data(
    old_data,
    new_data,
    output_filename=None
):

    combined_csv = pd.concat(
        [pd.read_csv(old_data), pd.read_csv(new_data)]
    )
    if not output_filename:
        combined_csv.to_csv(new_data)
    else:
        combined_csv.to_csv(output_filename)

    if os.path.exists(old_data):
        os.remove(old_data)

        # Print the statement once the file is deleted
        print("The file: {} is deleted!".format(old_data))
