-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3`
OPTIONS (
  format = 'Parquet',
  uris = ['gs://de_zoomcamp_test_bucket/green_taxi_data_week_3_hw.parquet']
);

SELECT count(*) FROM `peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3` ;

SELECT
  count(DISTINCT PULocationID)
FROM 
`peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3`;

SELECT
  count(DISTINCT PULocationID)
FROM 
`peppy-citron-411704.ny_taxi.green_taxi_hw_week_3`;

SELECT
  count(*)
FROM peppy-citron-411704.ny_taxi.green_taxi_hw_week_3
where fare_amount = 0;

CREATE OR REPLACE TABLE peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3_partitioned_by_pu_date_clustered_by_pu_location
PARTITION BY lpep_pickup_date
CLUSTER BY PUlocationID AS
SELECT * FROM peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3;

CREATE OR REPLACE TABLE peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3_clustered_by_pu_location_and_pu_date
CLUSTER BY lpep_pickup_date, PUlocationID AS
SELECT * FROM peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3;

CREATE OR REPLACE TABLE peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3_partitioned_by_pu_location_clustered_by_pu_date
PARTITION BY RANGE_BUCKET(PUlocationID, GENERATE_ARRAY(1, 1000000, 1000))
CLUSTER BY lpep_pickup_date AS
SELECT * FROM peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3;

select *
from peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3_partitioned_by_pu_date_clustered_by_pu_location
where lpep_pickup_date = '2022-01-01'
order by PUlocationID;

select *
from peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3_clustered_by_pu_location_and_pu_date
where lpep_pickup_date = '2022-01-01'
order by PUlocationID;

select *
from peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3_partitioned_by_pu_location_clustered_by_pu_date
where lpep_pickup_date = '2022-01-01'
order by PUlocationID;

select count(distinct PULocationID)
from peppy-citron-411704.ny_taxi.external_green_taxi_hw_week_3_partitioned_by_pu_date_clustered_by_pu_location
where lpep_pickup_date >= '2022-01-01' and lpep_pickup_date <= '2022-06-30';

select count(distinct PULocationID)
from peppy-citron-411704.ny_taxi.green_taxi_hw_week_3
where lpep_pickup_date >= '2022-01-01' and lpep_pickup_date <= '2022-06-30';