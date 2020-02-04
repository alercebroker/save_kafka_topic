# Save Kafka Topic

## Scripts

1) **download_topic.py** Ingest a specific topic and save avro to local filesystem
2) **concatenate_avros.py** Concatenate avro files into a few larger ones
3) **upload_to_s3.py** Upload result to S3
4) **service.py** Service driver, schedule to run scripts once every day

## Configuration

+ **kafka_server**: Kafka server domain name and port to ingest from (kafka1.alerce.online:9092)
+ **group**: Group name to identify Kafka's consumers (download)
+ **working_dir**: Working directory to download and process data (/tmp)
+ **output_bucket**: AWS S3 bucket to upload the results (s3://ztf-avro)
+ **start_time**: Start UTC time to start the whole process every day ("14:00")

## Deployment

1) **BUILD** Build docker image:
> ```docker build -t save_kafka_topic .```
2) **RUN** Run docker container and specify HOST_WORKING_DIR where kafka's topic is going to be downloaded and processed
>```docker run --detach --restart=always -v HOST_WORKING_DIR:/tmp --name save_kafka_topic save_kafka_topic```
3) **EXEC** Configure awscli key and password in order to upload data to S3 bucket 
>```docker exec -it save_kafka_topic /bin/bash ```

>  ```aws configure
   AWS Acess Key ID [None]: ID
   AWS Secret Access Key [None]: XXX
   Default region name [None]:
   Default output format [None]:
    ```
