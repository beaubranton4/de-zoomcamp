
## Week 5 Homework 


### Question 1: 

**Install Spark and PySpark** 

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?

-----

In my terminal, I ran

    pyspark
--

        spark = SparkSession.builder \
    ...     .appName("Local Spark Session") \
    ...     .getOrCreate()
--

	spark.version
> Answer: 3.5.0

### Question 2: 

**FHV October 2019**

Read the October 2019 FHV into a Spark Dataframe with a schema as we did in the lessons.

Repartition the Dataframe to 6 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 1MB
- 6MB
- 25MB
- 87MB


After creating parquet files in jupyter notebook - navigate to directory and execute ls -lh to see all files and file sizes. Code is in homework.ipynb

> Answer: 6MB

### Question 3: 

**Count records** 

How many taxi trips were there on the 15th of October?

Consider only trips that started on the 15th of October.

 - 108,164
- 12,856
- 452,470
-  62,610






    df = spark.read.parquet('data/pq/fhvhv/2019/10/')
    df \
        .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
        .filter("pickup_date = '2019-10-15'") \
        .count()
        


> Answer: 62,610

### Question 4: 

**Longest trip for each day** 

What is the length of the longest trip in the dataset in hours?

- 631,152.50 Hours
- 243.44 Hours
- 7.68 Hours
- 3.32 Hours

Ran this spark sql:

    spark.sql("""
    SELECT
        max((unix_timestamp(dropoff_datetime) - unix_timestamp(pickup_datetime)) / 3600) as hours_diff
    FROM 
        fhvhv_2019_10
    ;
    """).show()

Can also run this pyspark:

    df \
        .withColumn('duration', (df.dropoff_datetime.cast('long') - df.pickup_datetime.cast('long'))/3600) \
        .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
        .groupBy('pickup_date') \
            .max('duration') \
        .orderBy('max(duration)', ascending=False) \
        .limit(1) \
        .show()
    
> Answer: 631,152.5 Hours

### Question 5: 

**User Interface**

Spark’s User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080

> Answer: 4040


### Question 6: 

**Least frequent pickup location zone**

Load the zone lookup data into a temp view in Spark</br>
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?</br>

- East Chelsea
- Jamaica Bay
- Union Sq
- Crown Heights North

This code:

df.groupby('PULocationID').count().orderBy('count',ascending=True).limit(5).show()

showed me the answer was PULocationID = 2, which maps to...

> Answer: Jamaica Bay



