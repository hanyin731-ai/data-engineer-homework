from asyncio import run
import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq

# read urls
url_taxi = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
url_zone = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'


# read files
df_taxi = pd.read_parquet(url_taxi)
df_zone = pd.read_csv(url_zone)


# create engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# CREATE TBALE
df_taxi.head(0).to_sql(
            name="green_taxi_nov_data",
            con=engine,
            if_exists="replace")   

# INSERET DATA
df_taxi.to_sql(
        name="green_taxi_nov_data",
        con=engine,
        if_exists="append")

# CREATE TBALE
df_zone.head(0).to_sql(
            name="zone_data",
            con=engine,
            if_exists="replace")

# INSERET DATA
df_zone.to_sql(
        name="zone_data",
        con=engine,
        if_exists="append"
    )