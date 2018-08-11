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




#Funcion para crear la entidad en dynamoDB
def create_item(labels_object, labels_celebrities, periodico, idimagen):
    
    item = {
        'daymonthYear': utils.obtener_fecha_actual(),
        'idimagen': periodico + '/' + idimagen,
        'periodico': periodico,
        'Labels': utils.parsear_datos_object_escenes(labels_object),
        'CelebrityFaces': utils.parsear_datos_celebreties(labels_celebrities)
        }
    
    table.put_item(Item=item)



#Funcion para obtener las palabras por periodico
def obtener_nube_palabras_periodico(periodico):
    response = table.query(   
        KeyConditionExpression=Key('daymonthYear').eq(utils.obtener_fecha_actual()) & Key('idimagen').begins_with(periodico)
    )['Items']
    response = utils.parsear_datos_consulta(response)
    return response



