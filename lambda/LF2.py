import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
from boto3.dynamodb.conditions import Key
from variables import *


region = 'us-east-1' 
service = 'es'
lexbot = boto3.client('lexv2-runtime')

host = ES_URL
index = 'photos'
url = host + '/' + index + '/_search'

def lambda_handler(event, context):
    print(event)
    lexresponse = lexbot.recognize_text(
        botId = 'ZQ6QI2BI33',
        botAliasId = 'VJY77YHNUS',
        localeId='en_US',
        sessionId="test_session",
        text = event['queryStringParameters']['q']
        )
    print('lexresponse', lexresponse)
    print('lexresponse slot key word',lexresponse['sessionState']['intent']['slots']['PhotoType']['value']['originalValue'])
    query = {
        "size": 3,
        "query": {
            "multi_match": {
                "query": lexresponse['sessionState']['intent']['slots']['PhotoType']['value']['originalValue'],
                "fields": ['labels']
            }
        }
    }
    
    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    r = requests.get(url, auth=(USER, PASS), headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    print("es response", r.text)
    posts_list = json.loads(r.text)['hits']['hits']
    # posts_id_list = [x['_id'] for x in posts_list]
    
    response['body'] = json.dumps(posts_list)

    return response
