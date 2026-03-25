import json
import boto3
import csv
import io

s3 = boto3.client('s3')

BUCKET_NAME = "your-bucket-name"
FILE_KEY = "data/users.csv"

def lambda_handler(event, context):
    body = json.loads(event['body'])

    name = body['name']
    email = body['email']
    phone = body['phone']

    # Try to get existing CSV
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        csv_content = response['Body'].read().decode('utf-8')
        csv_file = io.StringIO(csv_content)
        reader = list(csv.reader(csv_file))
    except s3.exceptions.NoSuchKey:
        reader = [["Name", "Email", "Phone"]]  # Header

    # Append new row
    reader.append([name, email, phone])

    # Write back to CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(reader)

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=FILE_KEY,
        Body=output.getvalue()
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data stored successfully"})
    }