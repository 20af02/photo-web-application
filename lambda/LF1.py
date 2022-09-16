import json
import boto3
import requests
from datetime import datetime
from variables import *
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth


def detect_labels(bucket, key, min_conf=95):
    rek_client = boto3.client('rekognition', region_name='us-east-1',
                              aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    response = rek_client.detect_labels(
        Image={
            'S3Object':
            {'Bucket': bucket,
             'Name': key}
        },
        MinConfidence=min_conf, MaxLabels=10)
    return response['Labels']


def get_metadata(bucket, key):
    s3 = boto3.client('s3', region_name='us-east-1',
                      aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    response = s3.head_object(Bucket=bucket, Key=key)
    print(response)
    return response['Metadata']


def parse_labels(bucket, key, labels):
    labels_ = [x['Name'] for x in labels]
    metadata = get_metadata(bucket, key)
    if bool(metadata):
        metadata = metadata['customlabels'].split(',')
        labels_ = labels_ + metadata

    json_data = {
        "object_key": key,
        "bucket": bucket,
        "createdTimestamp": datetime.now().isoformat(),
        "labels": labels_
    }
    return json_data


def insert_into_ES(json_data):
    host = ES_URL
    url = host + 'photos/' + '_doc/' + json_data['object_key']
    headers = {'Content-Type': 'application/json'}
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY,
                       'us-east-1', 'es')
    response = requests.post(
        url, auth=awsauth, headers=headers, json=json_data)
    return response


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    print(event)

    B2 = event['Records'][0]['s3']["bucket"]["name"]
    file_name = event['Records'][0]['s3']["object"]["key"]
    labels = detect_labels(B2, file_name)
    json_data = parse_labels(B2, file_name, labels)
    response = insert_into_ES(json_data)
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps(response.json())
    }
