import os
import time
import uuid

import boto3
from boto3.dynamodb.types import DYNAMODB_CONTEXT
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
        'periodico': periodico,
        'idimagen': idimagen,
        'Labels': utils.parsear_datos_object_escenes(labels_object),
        'CelebrityFaces': utils.parsear_datos_celebreties(labels_celebrities)
        }
    
    table.put_item(Item=item)


