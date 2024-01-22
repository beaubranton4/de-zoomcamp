# Homework Week 1

## Question 1

Run: docker run --help

**Answer:**
> --rm

## Question 2

Run: 
docker run -it --entrypoint bash python:3.9

Then: 
pip list


**Answer:**
> 0.42.0

## Question 3


Use upload_hw_datasets.ipynb to upload data to postgres container

  

In PGAdmin: use the following SQL to obtain answer:

  

    select count(*) 
    from public.green_taxi_data 
    where date_trunc('day',lpep_pickup_datetime) = '2019-09-18'
    and date_trunc('day',lpep_dropoff_datetime) = '2019-09-18'

**Answer:**
> 15612

## Question 4



use the following SQL to obtain answer:

    select 
	    date_trunc('day',lpep_pickup_datetime) as pickup_day,    
	    sum(trip_distance)
    from green_taxi_data
    group by 1
    order by 2 desc
    limit 1

  
**Answer:**
> 2019-09-26


## Question 5



use the following SQL to obtain answer:

  

    select 
	    z."Borough",  
	    sum(total_amount) as total_amount  
    from green_taxi_data gt  
    left join zones z  
	    on gt."PULocationID" = z."LocationID" 
    where date_trunc('day',gt.lpep_pickup_datetime) = '2019-09-18' 
    group by 1
    order by 2 desc

  
**Answer:**
> "Brooklyn" "Manhattan" "Queens"

## Question 6

use the following SQL to obtain answer:

  

    select    
	    doz."Zone" as do_zone,    
	    max(tip_amount) as tips_total    
    from green_taxi_data gt    
    left join zones puz    
	    on gt."PULocationID" = puz."LocationID"    
    left join zones doz    
	    on gt."DOLocationID" = doz."LocationID"    
    where date_trunc('month',gt.lpep_pickup_datetime) = '2019-09-01'    
	    and puz."Zone" ilike '%Astoria%'
    group by 1
    order by 2 desc

  
**Answer:**
> JFK Airport



## Question 7

  

In the folder where we setup main.tf and variables.tf files for the Terraform lectures

Run: terraform apply

 
**Answer:**
```
>Terraform used the selected providers to generate the following execution plan. Resource actions
are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "de_zoomcamp_test_dataset_2"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "peppy-citron-411704"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "de_zoomcamp_test_bucket_2"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 2s [id=projects/peppy-citron-411704/datasets/de_zoomcamp_test_dataset_2]
google_storage_bucket.demo-bucket: Creation complete after 2s [id=de_zoomcamp_test_bucket_2]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```
