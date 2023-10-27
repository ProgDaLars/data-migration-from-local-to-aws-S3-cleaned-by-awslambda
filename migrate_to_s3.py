import boto3
import os
import glob

s3 = boto3.resource('s3')
dir_path = './'

# Get list of specific files for migration

#
# Create S3 bucket via CLI
# aws s3 mb s3://[unique-bucket-name]
#
# Create dynamoDB table in CLI
# aws dynamodb create-table --table-name cleaned_hotel_bookings --attribute-definitions AttributeName=hotel,AttributeType=S AttributeName=arrival_date,AttributeType=S --key-schema AttributeName=hotel,KeyType=HASH AttributeName=arrival_date,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region us-east-1

# NOTE: my key-schema is not unique, make yours unique to avoid your table rows from being overwritten by new entries in dynamoDB


csv_files = glob.glob(os.path.join(dir_path, '*.csv'))
#json_files = glob.glob(os.path.join(dir_path, '*.json'))
#all_files = csv_files + json_files

all_files = csv_files

# Iterate through list to upload objects to S3 
for rawfile in all_files:
    if rawfile.endswith('.csv'):
      try:
            file = open(rawfile, 'rb')
            file_name = os.path.basename(rawfile)
            object = s3.Object('practice-datasets','raw_datasets/' + file_name) 
            ret = object.put(Body=file,Metadata={'filename':file_name})
            print (file_name, " is uploaded")
      except Exception as e:
            print(f'Error uploading {file_name}: {str(e)}')

    #ret = object.put(Body=file,
     #               Metadata={'FullName':image[1]})
