# data-migration-from-local-to-aws-S3-cleaned-by-awslambda
This project demonstrates Data Migration/Ingestion from the local system to AWS

This Data Ingestion and Storage in AWS DynamoDB project is designed to showcase the process of ingesting data from a structured or semi-structured sources (csv and json), cleaning and transforming it on the fly with AWS Lambda python function and storing the cleaned data in S3 bucket as csv and json versions and as well storing it in an AWS DynamoDB database. 

DynamoDB is a fully managed, highly available, and scalable NoSQL database service provided by Amazon Web Services. 

The project involves the use of Python and the Boto3 library to interact with AWS services.

**Project AIM**

To scan specified directory for csv dataset, upload to S3, clean and transform dataset on the fly in AWS lambda function, upload two versions (csv and json) of the cleaned data into clean_datasets/ folder in S3 bucket and store the clean data into Amazon Dynamo DB


**Project Objectives:**

Data Source: The project begins with a structured dataset containing information related to hotel bookings. The dataset consists of various attributes such as hotel name, booking status, lead time, arrival date, guest information and more. The primary objective is to take this dataset, clean and transform it on the fly in AWS lambda function, store the cleaned version to S3 and also store it efficiently in DynamoDB.

Data Preparation: Prior to ingestion, the project addresses data preparation tasks. It includes data cleaning steps to handle outliers, duplicates and missing values - this was done on the fly in AWS lambda which was triggered on each file upload to the bucket. This ensures that the dataset is in a consistent and usable format for modelling and visualization.

AWS Setup: The project assumes the existence of an AWS environment. S3 bucket was created, lambda function was written, lambda layer was added and creation of a DynamoDB table. The required AWS permissions are defined in an IAM policy to allow the Lambda function to interact with the DynamoDB, Lambda and S3 services.

Data Ingestion: The core of the project is the development of a Python script to ingest the prepared dataset into DynamoDB. Boto3, the AWS SDK for Python, is used to interact with DynamoDB and S3. The script dynamically extracts column names from the dataset and uses them as attributes in DynamoDB, ensuring a flexible and scalable data insertion process.

**Summary**
1. Scan all csv dataset in local directory
2. Upload to a folder in Amazon S3 Bucket
3. Write a Lambda function in Python to clean and transform data
4. Trigger the lambda function as soon as data drops into the S3 bucket
5. Write the cleaned data (in **csv** and **json** formats) into another folder in Amazon S3 bucket
6. Store the cleaned data into Amazon Dynamo DB
7. END

   
**Technologies Used:**
- AWS (Amazon Web Services)
- S3 Bucket
- DynamoDB
- Python
- Boto3 (AWS SDK for Python)
