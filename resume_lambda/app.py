import json
import boto3
import logging
from decimal import Decimal
# import requests


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'visitorCountTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'

def lambda_handler(event, context):
    """Sample pure Lambda function
    """
    logger.info(event)
    
    httpMethod = event['httpMethod']
    countKey = ['visitsCount'] #event['queryStringParameters']['visitsCount']

    if httpMethod == getMethod:
        responseGet = getCurrentVisitorCount(countKey)
        if responseGet["body"]:
            response = updateVisitorCount(countKey, int(Decimal(responseGet["body"])))
        else:
            response = updateVisitorCount(countKey, 0)
    else:
         response = buildResponse(404, 'Unsupported Request')
    
    return response

def getCurrentVisitorCount(tablePrtKey):

    try:
        response = table.get_item(
            Key={
                'visitsCount': tablePrtKey
                })
        if 'Item' in response:
            return buildResponse(200, response['Item']['visitCountValue'])
        else:
            return buildResponse(404, {'Message':'Count value was not found'})
    except:
        logger.exception('Error retrieving value from DyanmoTable !!!')   

def updateVisitorCount(countKey, upDateValue):
    
    try:
        response = table.update_item(
        Key={
            'visitCount': countKey
        },
        UpdateExpression='SET visitCountValue = :increment',
        ExpressionAttributeValues={
            ':increment': upDateValue + 1
        })
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'CurrentCount': upDateValue + 1,
            'UpdateAttributes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Error in the updateVisitorCount function!!!')

def buildResponse(statusCode, body=None):

    return{
        'statusCode': statusCode,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
