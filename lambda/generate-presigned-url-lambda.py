import json
import boto3
import uuid
from botocore.config import Config

s3 = boto3.client(
    "s3",
    region_name="us-east-1",
    config=Config(signature_version="s3v4")
)

BUCKET_NAME = 'your-bucket-name'

def lambda_handler(event, context):
    # Handle preflight OPTIONS request
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "*"
            },
            "body": ""
        }


    params = event.get("queryStringParameters") or {}
    filename = params.get("filename")

    # CASE 1: No filename → return upload URL
    if not filename:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "filename required"})
        }

    # CASE 2: Check mode (NEW FEATURE)
    if params.get("checkThumbnail") == "true":

        key = f"Output/thumbnail-{filename}"

        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=key)

            url = s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": BUCKET_NAME,
                    "Key": key
                },
                ExpiresIn=300
            )

            return {
                "statusCode": 200,
                'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
                "body": json.dumps({
                    "status": "ready",
                    "url": url
                })
            }

        except:
            return {
                "statusCode": 200,
                'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
                "body": json.dumps({
                    "status": "processing"
                })
            }

    # CASE 3: Generate upload URL


    #params = event.get("queryStringParameters") or {}
    #file_name = params.get("filename", "file")

    key = f"Input/{uuid.uuid4()}-{filename}"
    stored_filename = key.replace("Input/", "")
    url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': key,
           
        },
        ExpiresIn=300
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({
            'uploadURL': url,
            'originalFileName':filename,
            'storedFileName': stored_filename # removed Input because while checking status it will go in Input folder so
        })
    }
