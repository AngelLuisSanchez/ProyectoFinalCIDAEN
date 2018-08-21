import os
import time
import uuid

import boto3
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key, Attr
import decimal
from handlers import utils

# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[decimal.Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[decimal.Rounded] = 0

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def create_item(labels_object, labels_celebrities, newspaper, idimage):
    item = {
        'daymonthYear': utils.get_current_date(),
        'idimagen': newspaper + '/' + idimage,
        'periodico': newspaper,
        'Labels': utils.parse_data_objects_and_scenes(labels_object),
        'CelebrityFaces': utils.parse_data_celebrities(labels_celebrities)
    }
    
    table.put_item(Item=item)

def get_cloud_tags_newspaper(periodico):
    response = table.query(   
        KeyConditionExpression=Key('daymonthYear').eq(utils.get_current_date()) & Key('idimagen').begins_with(periodico)
    )['Items']
    response = utils.parse_data_query(response)
    return response

def getCelebrities(paramDate):
    items = table.query(KeyConditionExpression=Key('daymonthYear').eq(utils.parse_date(paramDate)))['Items']
    celebrities = utils.parse_list_celebrities(items)
    return celebrities
