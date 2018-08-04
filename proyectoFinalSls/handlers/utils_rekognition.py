import json
import boto3

rekognition = boto3.client('rekognition', region_name='eu-west-1')


#Funcion para llamar reconocer celebridades
def recognize_celebrities(bucketName, filePath):
    response = rekognition.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': filePath
            }
        }
    )

    return response

#Funcion para un reconocimiento general de los elementos
def recognize_object_and_scenes(bucketName, filePath):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': filePath
            }
        }
    )

    return response

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

