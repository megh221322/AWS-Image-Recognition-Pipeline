SQS_LISTENER.PY(sqs_listener.py)
import boto3

def receive_messages_and_detect_text(bucket_name, queue_url):
    rekognition_client = boto3.client('rekognition')
    sqs_client = boto3.client('sqs')

    while True:
        messages = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20  # Long polling
        )

        if 'Messages' not in messages:
            print("No messages in queue. Waiting...")
            continue

        message = messages['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        image_key = message['Body']

        # Perform text detection
        response = rekognition_client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': image_key
                }
            }
        )

        print(f"Detected texts for {image_key}:")
        for text_detail in response['TextDetections']:
            print(text_detail['DetectedText'])

        # Delete the message from the queue
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

if _name_ == '_main_':
    BUCKET_NAME = 'njitcs643'  # Your S3 bucket name
    QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/294737378300/recogqueue'  # Your SQS queue URL

    receive_messages_and_detect_text(BUCKET_NAME, QUEUE_URL)
