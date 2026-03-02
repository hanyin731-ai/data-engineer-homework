"""dlt pipeline to ingest NYC taxi data from a REST API."""

import requests
import dlt
from typing import Iterator, Dict, Any


@dlt.resource(name="yellow_taxi_data", write_disposition="append")
def yellow_taxi_data() -> Iterator[Dict[str, Any]]:
    """Fetch yellow taxi data from REST API with pagination."""
    base_url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    
    while True:
        response = requests.get(
            f"{base_url}/yellow_taxi_data",
            params={"page": page, "page_size": 1000}
        )
        data = response.json()
        
        # Stop when an empty page is returned
        if not data or len(data) == 0:
            break
        
        # Yield each record
        for record in data:
            yield record
        
        page += 1


@dlt.resource(name="green_taxi_data", write_disposition="append")
def green_taxi_data() -> Iterator[Dict[str, Any]]:
    """Fetch green taxi data from REST API with pagination."""
    base_url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    
    while True:
        response = requests.get(
            f"{base_url}/green_taxi_data",
            params={"page": page, "page_size": 1000}
        )
        data = response.json()
        
        # Stop when an empty page is returned
        if not data or len(data) == 0:
            break
        
        # Yield each record
        for record in data:
            yield record
        
        page += 1


@dlt.source
def taxi_pipeline():
    """Define dlt resources for NYC taxi data."""
    return [yellow_taxi_data(), green_taxi_data()]


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name='taxi_pipeline',
        destination='duckdb',
        refresh="drop_sources",
        progress="log",
    )
    
    load_info = pipeline.run(taxi_pipeline())
    print(load_info)  # noqa: T201
