import uuid

from handlers import utils
from handlers import utils_dynamodb
from handlers import utils_rekognition

def image_uploaded(event, context):
    print('Event: ', event)
    file_obj = event['Records'][0]
    filePath = str(file_obj['s3']['object']['key'])
    fileName = filePath.split('celebrities/')[1]
    bucketName = file_obj['s3']['bucket']['name']
    
    print('bucketName', bucketName)
    print('filePath', filePath)
    
    response = utils_rekognition.recognize_celebrities(bucketName, filePath)
    print('response', response)

    if response["CelebrityFaces"]:
        image_uuid = str(uuid.uuid1())

        for celebrity in response["CelebrityFaces"]:
            utils_dynamodb.create(image_uuid, celebrity)

def dynamodb_celebrities(event, context):
    celebrities = utils_dynamodb.getCelebrities()

    print(celebrities)

    return utils.jsonify(celebrities)
