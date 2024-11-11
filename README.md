# AWS-Image-Recognition-Pipeline
This repository contains a setup for an image recognition pipeline built on AWS services including EC2, S3, SQS, and Rekognition. The pipeline automates downloading images, performing object detection, and text recognition on those images using AWS Rekognition.

## Project Overview

The pipeline is designed to process images stored in an S3 bucket using two EC2 instances. 

1. **EC2 Instance A**: This instance will download 10 images from an S3 bucket, perform object detection using AWS Rekognition to identify cars with a confidence level of more than 90%, and store the index of those images in an SQS queue.
   
2. **EC2 Instance B**: This instance will listen for messages from the SQS queue, fetch the corresponding image from the S3 bucket, and perform text detection using AWS Rekognition. The results will be stored in a file on an EBS volume attached to the instance.

The EC2 instances work in parallel, and once processing is completed, Instance A will add an index `-1` to the queue to signal to Instance B that no more images are available for processing.

## Prerequisites

- AWS account with access to EC2, S3, SQS, and Rekognition.
- Access to the AWS CLI.
- PEM key for SSH access to EC2 instances.
- The free-tier EC2 instances are sufficient for this task.
- Proper Security Group settings for EC2 instances (open SSH, HTTP, HTTPS).
