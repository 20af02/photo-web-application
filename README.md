# voice-controlled-photo-album-web-app
CS-GY 9223


## Overview:

Photo album web application searchable using natural language through both text and voice. Uses Lex, ElasticSearch, and Rekognition to create an intelligent search layer to query photos for people, objects, actions, landmarks, and more.
[Slide Summary]( https://docs.google.com/presentation/d/1AJLoqCY4bsoR1M8eWNmzm4pEYGzkx5Smb1yZeTP1fMo/edit?usp=sharing).


## Architecture:

<img width="1000" alt="Architecture diagram (1)" src="https://github.com/20af02/photo-web-application/blob/main/screenshots/architecture-diagram.jpg">


## Code Pipeline
<img width="1000" alt="CodePipeline diagram (2)" src="https://github.com/20af02/photo-web-application/blob/main/screenshots/code-pipeline-diagram.jpg">


## CloudFormation with Code Pipeline
<img width="1000" alt="CloudFormation diagram (3)" src="https://github.com/20af02/photo-web-application/blob/main/screenshots/cloud-formation-diagram.jpg">

Summary: 
Using the CloudFormation template (T1), the entire functional stack for this project is generated. Once a new commit is pushed to GitHub (for both lambda and frontend branches), CodePipeline builds and deploys code to the corresponding AWS infrastructure.


1.	The frontend for the application is hosted in an S3 bucket as a static website and through CloudFront CDN.
2.	Using the AWS ElasticSearch service, a domain is set up so that when a photo gets uploaded to the B2 bucket, a lambda function called 'Image Indexing Lambda' (LF1) is triggered for indexing.
3.	Labels are detected in the image using Rekognition, and users can input custom labels for any image uploaded. A JSON object with reference to each object in the S3 is stored in an ElasticSearch index for every label detected by the Rekognition service.
4.	A lambda function called 'Search Lambda' (LF2) is used as a code hook for the Lex service in order to detect the search keywords through natural language via voice and text.
5.	Amazon Lex bot is created to handle search queries for which an intent called 'SearchIntent' is created, and training utterances are added to the intent.
6.	For a given photo to be searched and a search query, a search returns every photo that matches the query. Specifically, if an image has _n_ labels, both custom and from Rekognition, Elasticsearch returns keys of the photo with any one of those labels as if searched independently
