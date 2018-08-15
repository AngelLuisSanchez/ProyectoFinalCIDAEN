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
    
    #Call API Rekognition to recognize objects and scenes
    response = utils_rekognition.recognize_object_and_scenes(bucketName, filePath)

    #Get results objects and scenes
    labels_object = utils.parse_results_objects_and_scenes(response, 'Labels')

    #Check labels for people
    size = len(labels_object) != 0
    personas = utils.check_for_people(labels_object)
    labels_celebrities = {}
    if(size and personas):
        #Call API Rekognition to recognize celebrities
        response = utils_rekognition.recognize_celebrities(bucketName, filePath)
        labels_celebrities = utils.parse_results_objects_and_scenes(response, 'CelebrityFaces')
    
    print(labels_object)
    print(labels_celebrities)
    
    #Save results into dynamo
    utils_dynamodb.create_item(labels_object, labels_celebrities, folder, fileName)

def download_images_elpais(event, context):
    utils_crawler.download_images_covers_newspaper('elpais', 'https://elpais.com/')
    os.listdir('/tmp/')
    utils_s3.move_to_s3_folder('elpais')

def download_images_elmundo(event, context):
    utils_crawler.download_images_covers_newspaper('elmundo', 'http://www.elmundo.es/')
    os.listdir('/tmp/')
    utils_s3.move_to_s3_folder('elmundo')

def download_images_abc(event, context):
    utils_crawler.download_images_covers_newspaper('abc', 'https://www.abc.es/')
    os.listdir('/tmp/')
    utils_s3.move_to_s3_folder('abc')

def download_images_diarioes(event, context):
    utils_crawler.download_images_covers_newspaper('diarioes', 'https://www.eldiario.es')
    os.listdir('/tmp/')
    utils_s3.move_to_s3_folder('diarioes')

def get_cloud_tags(event, context):
    newspapers = ['elpais', 'diarioes', 'elmundo', 'abc']
    cloudTags = []
    for p in newspapers:
        cloudTags.append({
            p: utils_dynamodb.get_cloud_tags_newspaper(p)
        })
    return utils.jsonify({'datos': cloudTags})

def list_celebrities(event, context):
    celebrities = utils_dynamodb.getCelebrities()

    return utils.jsonify({'datos': celebrities})

def s3_get_url(event, context):
    params = event['pathParameters']
    paramKey = params['key']
    keyaux = paramKey.replace('%2F', '/')

    print('key', keyaux)

    url = utils_s3.get_url(keyaux)

    return utils.jsonify({'url': url})
