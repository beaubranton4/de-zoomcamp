# Homework Week 2

## Question 1

Mage shows row count after running transformation

**Answer:**
> 266 855 rows x 20 columns

## Question 2

Mage shows row count after running transformation


**Answer:**
> -   139,370 rows

## Question 3



**Answer:**
> -   `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`

## Question 4



Run the following code to obtain unique values in vendor_id column:

print(data['vendor_id'].unique().tolist())

  
**Answer:**
1 or 2


## Question 5



Run print(data.columns) before transformation steps.

Following columns should be converted: 'VendorID', 'RatecodeID', 'PULocationID', 'DOLocationID',

  
**Answer:**
> 4

## Question 6

before exporting the data run: 

print(data['lpep_pickup_date'].nunique())

will provide unique values in the date column before it is chunked and uploaded to GCS

  
**Answer:**
> 95

