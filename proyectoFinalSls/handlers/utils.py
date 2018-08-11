import json
import datetime
import decimal
import random


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
        url = 'Nulo'
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


#Funcion para parsear las palabras de la nube
def parsear_datos_consulta(datos):
    d = []
    l1 = []
    for r in datos:
        if(len(r['Labels']) != 0):
            for l in r['Labels']:
                if l['Name'] not in l1:
                    l1.append(l['Name'])
                    d.append({
                        'text': l['Name'],
                        'weight' : float(l['Confidence']),
                        'color' : generar_color_aleatorio()
                        })
    return d

#Funcion para generar un color de forma aleatoria
def generar_color_aleatorio():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())
