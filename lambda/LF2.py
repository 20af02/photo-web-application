import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
from boto3.dynamodb.conditions import Key
from variables import *


region = 'us-east-1'
service = 'es'
lexbot = boto3.client('lexv2-runtime', region_name=region)

host = ES_URL
index = 'photos'
url = host + '/' + index + '/_search'


def lambda_handler(event, context):
    print("event: ")
    print(event)
    print(json.dumps(event))
    query_text = event['queryStringParameters']['q']
    lexresponse = lexbot.recognize_text(
        botId='QCIT86RV12',
        botAliasId='RWJALIEWCV',
        localeId='en_US',
        sessionId="test_session",
        text=query_text
    )
    print('lexresponse', lexresponse)
    if lexresponse['sessionState']['intent']['slots'] == {}:
        res_ = query_text
    else:
        res_ = lexresponse['sessionState']['intent']['slots']['PhotoType']['value']['originalValue']
    print('lexresponse slot key word',
          res_)

    key_word_list = res_.replace(' and', '').split()

    headers = {"Content-Type": "application/json"}

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Headers": '*',
            "Access-Control-Allow-Methods": '*'
        },
    }

    final_url_list = []

    for term in key_word_list:
        url_list = []
        query = {"query": {
            "bool": {
                "must": [
                    {"fuzzy": {
                        "labels": {
                            "value": term}
                    }
                    }
                ]
            }
        },
            "size": 10}

        # Make the signed HTTP request
        r = requests.get(url, auth=(USER, PASS),
                         headers=headers, data=json.dumps(query))

        print("es response", r.text)
        posts_list = json.loads(r.text)['hits']['hits']

        url_list = ['https://s3.amazonaws.com/' +
                    str(x["_source"]["bucket"]) + '/' + str(x["_source"]["object_key"]) for x in posts_list]

        final_url_list += url_list

    final_url_list = list(set(final_url_list))
    response['body'] = json.dumps(final_url_list)

    return response
