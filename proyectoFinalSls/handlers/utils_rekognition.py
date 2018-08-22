import json
import boto3

rekognition = boto3.client('rekognition', region_name='eu-west-1')

#Function to recognize celebrities
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

#Function to recognize objects and scenes
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
