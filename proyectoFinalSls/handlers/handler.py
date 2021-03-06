import uuid
import os

from handlers import utils
from handlers import utils_dynamodb
from handlers import utils_rekognition
from handlers import utils_crawler
from handlers import utils_s3

def image_uploaded(event, context):

    for e in event['Records']:
        file_obj = e
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
        print("----------------------")
        
        #Save results into dynamo
        utils_dynamodb.create_item(labels_object, labels_celebrities, folder, fileName)

def download_images(event, context):
    periodicos = ['elpais', 'elmundo' , 'abc', 'diarioes']
    url_periodicos = ['https://elpais.com/', 'http://www.elmundo.es/', 'https://www.abc.es/', 'https://www.eldiario.es']

    for i in range(len(periodicos)):
        utils_crawler.download_images_covers_newspaper(periodicos[i], url_periodicos[i])
        utils_s3.move_to_s3_folder(periodicos[i])

def get_cloud_tags(event, context):
    newspapers = ['elpais', 'diarioes', 'elmundo', 'abc']
    cloudTags = []
    for newspaper in newspapers:
        cloudTags.append({
            newspaper: utils_dynamodb.get_cloud_tags_newspaper(newspaper)
        })
    return utils.jsonify({'cloudTags': cloudTags})

def list_celebrities(event, context):
    params = event['pathParameters']
    paramDate = params['date']

    celebrities = utils_dynamodb.getCelebrities(paramDate)

    return utils.jsonify({'celebrities': celebrities})

def s3_get_url(event, context):
    params = event['pathParameters']
    paramKey = params['key']
    keyaux = paramKey.replace('%2F', '/')

    url = utils_s3.get_url(keyaux)

    return utils.jsonify({'url': url})

def countCelebritiesByNewspaper(event, context):
    counterCelebrities = utils_dynamodb.getCountCelebritiesByNewspaper()

    return utils.jsonify({'counterCelebrities': counterCelebrities.__dict__})
