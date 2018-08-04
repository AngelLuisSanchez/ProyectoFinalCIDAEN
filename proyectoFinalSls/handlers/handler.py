import uuid

from handlers import utils
from handlers import utils_dynamodb
from handlers import utils_rekognition

def image_uploaded(event, context):

    file_obj = event['Records'][0]
    filePath = str(file_obj['s3']['object']['key'])
    fileName = filePath.split('input_images/')[1]
    bucketName = file_obj['s3']['bucket']['name']
    

    #Llamamos a la api que reconoce objetos y escenas
    response = utils_rekognition.recognize_object_and_scenes(bucketName, filePath)

    #Vemos si hay resultados
    labels_object = utils_rekognition.parsear_resultado_object_and_scenes(response, 'Labels')

    #Comprobamos si hay labels y si existen personas en ellas
    size = len(labels_object) != 0
    personas = utils_rekognition.comprobar_si_hay_persona(labels_object)
    labels_celebrities = {}
    if(size and personas):
        #LLamamos a la api de celebridades
        response = utils_rekognition.recognize_celebrities(bucketName, filePath)
        labels_celebrities = utils_rekognition.parsear_resultado_object_and_scenes(response, 'CelebrityFaces')
    
    print(labels_object)
    print(labels_celebrities)
    
    #Guardamos los resultados en dynamo
    #metodo para hacerlo
    


def dynamodb_celebrities(event, context):
    celebrities = utils_dynamodb.getCelebrities()

    print(celebrities)

    return utils.jsonify(celebrities)
