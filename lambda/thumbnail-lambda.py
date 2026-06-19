import json
import boto3
from PIL import Image
import os
import io

s3 = boto3.client('s3')

THUMBNAIL_SIZE = (128, 128)

def lambda_handler(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    print("bucket_name=", bucket_name)
    object_key = event['Records'][0]['s3']['object']['key']

    # Only process files inside input/
    if not object_key.startswith('Input/'):
        return

    filename = object_key.split('/')[-1]

    print(filename)
    # Download image from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)

    image_content = response['Body'].read()

    # Open image
    image = Image.open(io.BytesIO(image_content))

    # Create thumbnail
    image.thumbnail(THUMBNAIL_SIZE)

    # Save thumbnail to memory
    buffer = io.BytesIO()

    image.save(buffer, image.format)

    buffer.seek(0)

    # Upload thumbnail to output folder
    output_key = f'Output/thumbnail-{filename}'

    s3.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=buffer,
        ContentType=response['ContentType']
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Thumbnail created successfully')
    }
