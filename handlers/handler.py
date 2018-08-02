import json

def image_uploaded(event, context):
    print('Event: ', event)
    file_obj = event['Records'][0]
    filePath = str(file_obj['s3']['object']['key'])
    fileName = filePath.split('celebrities/')[1]
    bucketName = file_obj['s3']['bucket']['name']

    print('fileName', fileName)
    print('bucketName', bucketName)

    
