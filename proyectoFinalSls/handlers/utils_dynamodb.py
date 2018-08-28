import os
import time
import uuid

import boto3
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key, Attr
import decimal
from handlers import utils
from classes import CounterCelebrities

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
    items = table.query(   
        KeyConditionExpression=Key('daymonthYear').eq(utils.get_current_date()) & Key('idimagen').begins_with(newspaper)
    )['Items']
    wordCloudList = utils.parse_data_cloud_tag(items)

    wordCloud = [cloudTag.serialize() for cloudTag in wordCloudList]

    return wordCloud

def getCelebrities(paramDate):
    items = table.query(KeyConditionExpression=Key('daymonthYear').eq(utils.parse_date(paramDate)))['Items']
    listCelebrities = utils.parse_list_celebrities(items)

    abcItemsByDate = table.query(KeyConditionExpression=Key('daymonthYear').eq(
        utils.parse_date(paramDate)) & Key('idimagen').begins_with('abc'))['Items']
    elmundoItemsByDate = table.query(KeyConditionExpression=Key('daymonthYear').eq(
        utils.parse_date(paramDate)) & Key('idimagen').begins_with('elmundo'))['Items']
    diarioesItemsByDate = table.query(KeyConditionExpression=Key('daymonthYear').eq(
        utils.parse_date(paramDate)) & Key('idimagen').begins_with('diarioes'))['Items']
    elpaisItemsByDate = table.query(KeyConditionExpression=Key('daymonthYear').eq(
        utils.parse_date(paramDate)) & Key('idimagen').begins_with('elpais'))['Items']

    counterCelebrities = CounterCelebrities.CounterCelebrities(
        utils.countCelebrities(abcItemsByDate),
        utils.countCelebrities(elmundoItemsByDate),
        utils.countCelebrities(elpaisItemsByDate),
        utils.countCelebrities(diarioesItemsByDate)
    )

    celebrities = [celebrity.serialize() for celebrity in listCelebrities]

    obj = {
        'listCelebrities': celebrities,
        'counterCelebrities': counterCelebrities.__dict__
    }

    return obj

def getCountCelebritiesByNewspaper():
    abcItems = table.scan(FilterExpression=Key('idimagen').begins_with('abc'))['Items']
    elmundoItems = table.scan(FilterExpression=Key('idimagen').begins_with('elmundo'))['Items']
    diarioesItems = table.scan(FilterExpression=Key('idimagen').begins_with('diarioes'))['Items']
    elpaisItems = table.scan(FilterExpression=Key('idimagen').begins_with('elpais'))['Items']

    counterCelebrities = CounterCelebrities.CounterCelebrities(
        utils.countCelebrities(abcItems),
        utils.countCelebrities(elmundoItems),
        utils.countCelebrities(elpaisItems),
        utils.countCelebrities(diarioesItems)
    )

    return counterCelebrities
