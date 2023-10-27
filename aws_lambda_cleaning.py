from __future__ import print_function
import json
import pandas as pd
import boto3
from io import StringIO

s3 = boto3.client('s3')
bucket_name = 'practice-datasets'

dynamodb = boto3.client('dynamodb')
table_name = 'cleaned_hotel_bookings'

def save_to_dynamodb(df,table_name):
    try:
        attributes = df.columns
        for index, row in df.iterrows():
            item = {}
            for attribute in attributes:
                item[attribute] = {"S": str(row[attribute])}
        
            response = dynamodb.put_item(
                TableName=table_name,
                Item=item
            )
    except Exception as e:
        print(f'Error: {str(e)}')
        
    
def lambda_handler(event, context):
    try:
        # Get the object from the S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print("Processing object:", key)
        # Read the data from the S3 object
        payload = s3.get_object(Bucket=bucket, Key=key)
        raw_data = payload['Body'].read().decode('utf-8')
        filename = payload['Metadata']['filename']
        print("Object bucket:", bucket)
        
        # Data Cleaning
        hotel = pd.read_csv(StringIO(raw_data))
        
        # Remove rows with specific criteria (outliers)
        print("Preparing to remove outliers")
        booking_outlier = (hotel['adults'] == 0) & (hotel['children'] == 0) & (hotel['babies'] == 0) #outliers
        hotel = hotel[~booking_outlier]
        print(f"{len(hotel[booking_outlier])} outliers/irrelevant entries removed from hotel datasets")
        
        
        # Remove duplicate rows
        duplicate_values = hotel.duplicated().any()
        if duplicate_values.any():
            hotel.drop_duplicates(inplace=True)
            print(f"{hotel.duplicated().sum()} duplicate entries removed from hotel datasets.")

        
        # Create new date-related columns
        month_mapping = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        hotel['arrival_date_month_index'] = hotel['arrival_date_month'].replace(month_mapping)
        hotel['arrival_date'] = hotel['arrival_date_year'].astype(str) + '-' + hotel['arrival_date_month_index'].astype(str) + '-' + hotel['arrival_date_day_of_month'].astype(str)
        
        # Calculate the total number of guests
        hotel['total_guests'] = hotel['adults'] + hotel['children'] + hotel['babies']
        
        # Fill NULL values in the 'company' column with 0
        null_values = hotel.isna().any()
        if null_values.any():
            hotel['company'].fillna(0, inplace=True)
            print(f"{hotel.duplicated().sum()} duplicate entries removed from hotel datasets.")

        # Prepare cleaned data for upload
        cleaned_data = hotel.to_csv(index=False)
        json_data = hotel.to_json(orient='records')
        json_filename = filename + '.json'
        
        # Define the new object key for the cleaned data
        cleaned_data_key = 'clean_datasets/' + filename
        json_data_key = 'clean_datasets/' + json_filename
        
        # Upload the cleaned data to a new S3 location
        s3.put_object(Bucket=bucket_name, Key=cleaned_data_key, Body=cleaned_data)
        s3.put_object(Bucket=bucket_name, Key=json_data_key, Body=json_data)
        
        clean_csv_file = StringIO(cleaned_data) #convert to datafreme pandas can read
        cleaned_hotel_df = pd.read_csv(clean_csv_file)
        save_to_dynamodb(cleaned_hotel_df,table_name)
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Hotel dataset cleaning succeeded and uploaded to S3: {cleaned_data_key}!')
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'message': json.dumps(f'Error: {str(e)}')
        }
