# Save Kafka Topic
Here we describe the **Save Kafka Topic** service. It is encapsulated in a Docker container and consists mainly of a series of scripts that are explained as following:

## Scripts

1) **download_topic.py** Ingest a specific topic and save avro files to local filesystem

```
python3 download_topic.py KAFKA_SERVER KAFKA_TOPIC OUTPUT_DIR KAFKA_GROUP
```

2) **concatenate_avros.py** Concatenate avro files into a few larger ones of avro's chunks of 2200 of size each:

```
python3 concatenate_avros.py INPUT_DIRECTORY OUTPUT_DIRECTORY
```

3) **upload_to_s3.py** Upload result to an S3 bucket using aws command line program:

```
python3 upload_to_s3.py INPUT_DIR S3_BUCKET_PATH
```

4) **service.py** Service driver, schedule to run scripts once every day inside a Docker using a configuration file.
It use the preceding scripts in order: (1) download_topic.py , (2) concatenate_avros.py and finally (3) upload_to_s3.py.


## Configuration

You can change the configuration file **conf.json** containing the following parameters:

+ **kafka_server**: Kafka server domain name and port to ingest from (kafka1.alerce.online:9092)
+ **group**: Group name to identify Kafka's consumers (download)
+ **working_dir**: Working directory to download and process data (/tmp)
+ **output_bucket**: AWS S3 bucket to upload the results (s3://ztf-avro)
+ **start_time**: Start UTC time to start the whole process every day ("14:00")

## Deployment

Clone the repository, change to the directory and execute:

1) **BUILD** Build docker image:
> ```docker build -t save_kafka_topic .```
2) **RUN** Run docker container and specify HOST_WORKING_DIR where kafka's topic is going to be downloaded and processed
>```docker run --detach --restart=always -v HOST_WORKING_DIR:/tmp --name save_kafka_topic save_kafka_topic```
3) **EXEC** Configure awscli key and password in order to upload data to S3 bucket 
>```docker exec -it save_kafka_topic /bin/bash ```

>  ```aws configure ``` <br/>
>   AWS Acess Key ID [None]: KEY <br/>
>   AWS Secret Access Key [None]: PASSWORD <br/>
>   Default region name [None]: <br/>
>   Default output format [None]: <br/>
   
