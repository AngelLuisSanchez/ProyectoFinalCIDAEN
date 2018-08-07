import uuid
import os

from handlers import utils
from handlers import utils_dynamodb
from handlers import utils_rekognition
from handlers import utils_crawler
from handlers import utils_s3

def image_uploaded(event, context):

    file_obj = event['Records'][0]
    filePath = str(file_obj['s3']['object']['key'])
    folder = filePath.split('/')[0]
    fileName = filePath.split('/')[1]
    bucketName = file_obj['s3']['bucket']['name']
    

    #Llamamos a la api que reconoce objetos y escenas
    response = utils_rekognition.recognize_object_and_scenes(bucketName, filePath)

    #Vemos si hay resultados
    labels_object = utils.parsear_resultado_object_and_scenes(response, 'Labels')

    #Comprobamos si hay labels y si existen personas en ellas
    size = len(labels_object) != 0
    personas = utils.comprobar_si_hay_persona(labels_object)
    labels_celebrities = {}
    if(size and personas):
        #LLamamos a la api de celebridades
        response = utils_rekognition.recognize_celebrities(bucketName, filePath)
        labels_celebrities = utils.parsear_resultado_object_and_scenes(response, 'CelebrityFaces')
    
    print(labels_object)
    print(labels_celebrities)
    
    #Guardamos los resultados en dynamo
    utils_dynamodb.create_item(labels_object, labels_celebrities, folder, fileName)



def descargar_imagenes_elpais(event, context):
    utils_crawler.images_el_pais()
    os.listdir('/tmp/')
    utils_s3.move_to_s3_folder('elpais')

def descargar_imagenes_elmundo(event, context):
    utils_crawler.images_el_mundo()
    os.listdir('/tmp/')
    utils_s3.move_to_s3_folder('elmundo')

    

