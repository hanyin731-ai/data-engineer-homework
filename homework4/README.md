# data-engineer-homework

My Data Engineer Zoomcamp Homework 4

---

## Question 3. Counting Records in fct_monthly_zone_revenue
After running your dbt project, query the fct_monthly_zone_revenue model.
What is the count of records in the fct_monthly_zone_revenue model?
```sql
--fct_monthly_zone_revenue
SELECT count(*) FROM `tensile-proxy-486113-u3.dbt_hxue.fct_monthly_zone_revenue` --15579
;
```

## Question 4. Best Performing Zone for Green Taxis (2020)
Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020.
Which zone had the highest revenue?
```sql
SELECT pickup_zone, revenue_monthly_total_amount FROM `tensile-proxy-486113-u3.dbt_hxue.fct_monthly_zone_revenue` 
where service_type = 'Green' and EXTRACT(YEAR FROM revenue_month) = 2020
order by revenue_monthly_total_amount desc
limit 10
;
```

## Question 5. Green Taxi Trip Counts (October 2019)
Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?
```sql
select SUM(total_monthly_trips)
from `tensile-proxy-486113-u3.dbt_hxue.fct_monthly_zone_revenue` 
where service_type = 'Green' and EXTRACT(YEAR FROM revenue_month) = 2019 and EXTRACT(MONTH FROM revenue_month) = 10
;
```

## Question 6. Build a Staging Model for FHV Data
Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019.

 - Load the FHV trip data for 2019 into your data warehouse
   - data loaded via web_to_gcs
   - create external table 
   ```sql
    CREATE OR REPLACE EXTERNAL TABLE `tensile-proxy-486113-u3.zoomcamp.fhv_tripdata`
    OPTIONS (
    format = 'Parquet',
    uris = ['gs://hanyin-kestra-zoomcamp/fhv/fhv_tripdata_2019-*.parquet']
    );


    SELECT count(*) FROM `tensile-proxy-486113-u3.zoomcamp.fhv_tripdata`;
    ```
 - Create a staging model stg_fhv_tripdata with these requirements:
   - Filter out records where dispatching_base_num IS NULL
   - Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)
   - Finish the above 2 steps in https://github.com/hanyin731-ai/dbt-zoomcamp/blob/main/models/staging/stg_fhv_tripdata.sql

What is the count of records in stg_fhv_tripdata?
```SQL
SELECT COUNT(*) FROM `tensile-proxy-486113-u3.dbt_hxue.stg_fhv_tripdata`
```
