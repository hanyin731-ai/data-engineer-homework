```sql
 -- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `terraform-485315.my_dataset.external_yellow_tripdata`
OPTIONS (
  format = 'Parquet',
  uris = ['gs://terraform-485315-terra-bucket/yellow_tripdata_*.parquet']
);

 -- Creating table referring to gcs path
CREATE OR REPLACE TABLE `terraform-485315.my_dataset.internal_yellow_tripdata` AS
SELECT * FROM `terraform-485315.my_dataset.external_yellow_tripdata`;

-- Q1 Counting records
-- What is count of records for the 2024 Yellow Taxi Data?
SELECT COUNT(*) FROM `terraform-485315.my_dataset.internal_yellow_tripdata`;

SELECT COUNT(*) FROM `terraform-485315.my_dataset.external_yellow_tripdata`;

-- Q2 Data read estimation
-- Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
-- What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
SELECT COUNT(DISTINCT PULocationID) FROM `terraform-485315.my_dataset.internal_yellow_tripdata`;

SELECT COUNT(DISTINCT PULocationID) FROM `terraform-485315.my_dataset.external_yellow_tripdata`;

-- Question 3. Understanding columnar storage
-- Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.
-- Why are the estimated number of Bytes different?
SELECT PULocationID FROM `terraform-485315.my_dataset.internal_yellow_tripdata`;
SELECT PULocationID,DOLocationID FROM `terraform-485315.my_dataset.internal_yellow_tripdata`;

--Question 4. How many records have a fare_amount of 0?
SELECT COUNT(*) FROM `terraform-485315.my_dataset.internal_yellow_tripdata` WHERE fare_amount = 0;

-- Question 5. What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy) 
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE `terraform-485315.my_dataset.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `terraform-485315.my_dataset.external_yellow_tripdata`;

-- Question 6. Partition benefits
-- Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
-- Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?
SELECT DISTINCT VendorID
FROM `terraform-485315.my_dataset.yellow_tripdata_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';

SELECT DISTINCT VendorID
FROM `terraform-485315.my_dataset.internal_yellow_tripdata`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';

-- Question 9. Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why? 
SELECT COUNT(*) FROM `terraform-485315.my_dataset.internal_yellow_tripdata`;

```