# data-engineer-homework

My Data Engineer Zoomcamp Homework

---

## Question 1. Understanding Docker images

Run docker with the `python:3.13` image. Use an entrypoint bash to interact with the container.

### What's the version of pip in the image?

---

### Code

```bash
(base) xuehanyin@setsus-MacBook-Pro data-engineer-homework % docker run -it --entrypoint=bash  python:3.13
Unable to find image 'python:3.13' locally
3.13: Pulling from library/python
26d823e3848f: Pull complete 
82e18c5e1c15: Pull complete 
b6513238a015: Pull complete 
be442a7e0d6f: Pull complete 
9b57076d00d4: Pull complete 
2ca1bfae7ba8: Pull complete 
ca4b54413202: Pull complete 
9a005bc08170: Download complete 
1b9b364b83a0: Download complete 
Digest: sha256:c8b03b4e98b39cfb180a5ea13ae5ee39039a8f75ccf52d6d5c216eed6e1be1d
Status: Downloaded newer image for python:3.13
```

Answer: 25.3
```bash
root@91c2c787fcf8:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

---

## Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

---

```bash
select count(*) , max(lpep_pickup_datetime), min(lpep_pickup_datetime)
from green_taxi_nov_data
where lpep_pickup_datetime between '2025-11-01' and '2025-12-01'
and trip_distance <= 1;
```


##  Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

```bash
select lpep_pickup_datetime
from green_taxi_nov_data
where trip_distance <= 100
order by trip_distance desc
limit 1
;
```

##  Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?
```bash
select "Zone", sum("total_amount")
from green_taxi_nov_data taxi
left join zone_data 
 on taxi."PULocationID" = zone_data."LocationID"
where date("lpep_pickup_datetime") = '2025-11-18'
group by 1
order by sum("total_amount") desc
limit 1
;
```

##  Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?
```bash
select drop_off_zone."Zone", max("tip_amount")
from green_taxi_nov_data taxi
left join zone_data pick_up_zone
 on taxi."PULocationID" = pick_up_zone."LocationID"
left join zone_data drop_off_zone
 on taxi."DOLocationID" = drop_off_zone."LocationID"
where pick_up_zone."Zone" = 'East Harlem North'
and to_char("lpep_pickup_datetime", 'YYYY-MM') = '2025-11'
group by 1
order by max("tip_amount") desc
limit 1
;
```
