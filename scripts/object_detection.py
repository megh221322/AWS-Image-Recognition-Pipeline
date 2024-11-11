import boto3
import os
import json
from PIL import Image
import requests
from io import BytesIO

# AWS configuration
S3_BUCKET = 'njitcs643'
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/294737378300/recogqueue'

# Initialize AWS clients
rekognition_client = boto3.client('rekognition')
sqs_client = boto3.client('sqs')
s3_client = boto3.client('s3')

def detect_objects(image_key):
    """Detect objects in an image."""
    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': S3_BUCKET,
                'Name': image_key
            }
        },
        MaxLabels=10,
        MinConfidence=90
    )
    return response['Labels']

def process_images():
    """Process images from S3 bucket."""
    # List images in the S3 bucket
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
    if 'Contents' not in response:
        print("No images found in the bucket.")
        return

    for item in response['Contents']:
        image_key = item['Key']
        print(f"Processing {image_key}...")

        # Detect objects in the image
        labels = detect_objects(image_key)
        for label in labels:
            if label['Name'] == 'Car':
                print(f"Detected car in {image_key} with confidence {label['Confidence']:.2f}%")
                # Send the image key to SQS
                send_to_sqs(image_key)

def send_to_sqs(image_key):
    """Send the image key to SQS."""
    response = sqs_client.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=image_key
    )
    print(f"Sent {image_key} to SQS.")

if _name_ == '_main_':
    process_images()
