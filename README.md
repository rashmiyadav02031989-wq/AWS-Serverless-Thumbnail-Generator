# AWS-Serverless-Thumbnail-Generator

## Overview
A fully serverless image processing system that automatically generates thumbnails when users upload images to Amazon S3. The system uses AWS Lambda triggered by S3 events and stores processed thumbnails in a separate output folder.

## Architecture
```mermaid
flowchart TD

A[User] --> B[Frontend - S3 Static Website Bucket]

B --> C[S3 Bucket: Input Folder]
C --> D[S3 Event Trigger]

D --> E[AWS Lambda Function<br/>Thumbnail Generator]

E --> F[Download Image from S3 Input Folder]
F --> G[Process Image<br/>Generate Thumbnail]

G --> H[Upload Thumbnail to S3 Output Folder]

H --> I[User Views Output Thumbnails via S3 / CloudFront]

subgraph S3_Buckets
C
H
end

subgraph AWS_Serverless
D
E
F
G
end
```
## AWS Services Used
- Amazon S3
- AWS Lambda
- IAM Roles
- (Optional) CloudFront for frontend hosting

## Features
- Automatic thumbnail generation
- Event-driven processing (S3 → Lambda)
- Separate input and output storage
- Scalable serverless architecture

## Repository Structure
```text
lambda/ - AWS Lambda function code
frontend/ - HTML UI for uploading images
screenshots/ - Project UI and output images
architecture/ - System architecture diagram
