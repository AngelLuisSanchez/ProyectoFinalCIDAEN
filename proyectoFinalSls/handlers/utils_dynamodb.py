import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def getCelebrities():
    return table.scan()['Items']
  
def read(id):
    res = table.get_item(
        Key={
            'id': id
        }
    )

    return res['Item'] if 'Item' in res else None

def create(image_uuid, celebrity):
    timestamp = str(int(time.time() * 1000))
    item = {
        'id': str(uuid.uuid4()),
        'idImage': image_uuid,
        'idCelebrity': celebrity['Id'],
        'name': celebrity['Name'],
        'url': celebrity['Urls'][0] if celebrity['Urls'] else '-',
        #Si no viene url, deberia poner None, pero dynamo pone true, ¿que ponemos si no trae url? un guion? vacio?
        'createdAt': timestamp
    }

    table.put_item(Item=item)

# EJEMPLO ITEM A GUARDAR
# {'createdAt': '1533338638369',
#  'id': '3ed1eba8-4106-4da0-98fd-97f2374f08fa',
#  'idCelebrity': '2So4RX0w',
#  'idImage': '4c1bd5ea-9774-11e8-8dbf-0242ac110002',
#  'name': 'Justin Trudeau',
#  'url': 'www.imdb.com/name/nm0874040'}
