import json
import datetime
import decimal


def jsonify(obj):
    return {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'statusCode': 200,
        'body': json.dumps(obj)
    }


#Funcion para saber si es necesario llamar a la api de celebridades
def comprobar_si_hay_persona(labels):

    names = ['Human', 'People', 'Person', 'Face']

    for label in labels:
        if(label['Name'] in names):
            return True
    
    return False


#Funcion para saber si la api trae resultados
def parsear_resultado_object_and_scenes(response, label):

    try:
        if((label in response) and (len(response[label]) != 0)):
            return response[label]
        else:
            return {}
    except:
        print('No hay labels')
        return {}


#Funcion para obtener el dia mes y anno actual que servira como clave para la bbdd
def obtener_fecha_actual():
    dia = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%m")
    year = datetime.datetime.now().strftime("%Y")
    return str(dia)+str(month)+str(year)


#Funcion para parsear los datos de la api object and scenes
def parsear_datos_object_escenes(labels_object):
    datos = []
    for label in labels_object:
        datos.append(
            {
                'Name': label['Name'],
                'Confidence': decimal.Decimal(str(label['Confidence']))
            }
        )
    return datos


#Funcion para parsear los datos de la api de celebreties
def parsear_datos_celebreties(labels_celebrities):
    datos = []
    for label in labels_celebrities:
        url = ''
        if('Urls' in label and len(label['Urls']) != 0):
            url = label['Urls'][0]
        datos.append(
            {
                'Name': label['Name'],
                'Id': label['Id'],
                'Url': url
            }
        )
    return datos
