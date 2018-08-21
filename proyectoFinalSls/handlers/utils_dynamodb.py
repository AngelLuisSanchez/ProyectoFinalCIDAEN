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

def get_cloud_tags_newspaper(newspaper):
    response = table.query(   
        KeyConditionExpression=Key('daymonthYear').eq(utils.get_current_date()) & Key('idimagen').begins_with(newspaper)
    )['Items']
    response = utils.parse_data_query(response)
    return response

def getCelebrities(paramDate):
    items = table.query(KeyConditionExpression=Key('daymonthYear').eq(utils.parse_date(paramDate)))['Items']
    celebrities = utils.parse_list_celebrities(items)
    return celebrities

def getCountCelebritiesByNewspaper():
    abcItems = table.scan(FilterExpression=Key('idimagen').begins_with('abc'))['Items']
    elmundoItems = table.scan(FilterExpression=Key('idimagen').begins_with('elmundo'))['Items']
    diarioesItems = table.scan(FilterExpression=Key('idimagen').begins_with('diarioes'))['Items']
    elpaisItems = table.scan(FilterExpression=Key('idimagen').begins_with('elpais'))['Items']

    counts = {
        'abc': utils.countCelebrities(abcItems),
        'elmundo': utils.countCelebrities(elmundoItems),
        'diarioes': utils.countCelebrities(diarioesItems),
        'elpais': utils.countCelebrities(elpaisItems)
    }

    return counts