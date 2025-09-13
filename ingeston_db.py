import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory2.db')

def ingest_db(df, table_name, engine):
    """This function ingests the dataframe into a database table."""
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

def load_raw_data():
    """This function will load the CSVs as dataframes and ingest them into the db."""
    start = time.time()
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join('data', file))
            logging.info(f'Ingesting {file} into db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end - start) / 60
    logging.info('---------------Ingestion Complete---------------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')

if __name__ == '__main__':
    load_raw_data()
