import json
import boto3

rekognition = boto3.client('rekognition', region_name='eu-west-1')

def recognize_celebrities(bucketName, filePath):
    response = rekognition.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': filePath
            }
        }
        #"MinConfidence": 50
    )

    return response

#EJEMPLO RESPONSE DE LA API REKOGNITION
# {'CelebrityFaces': [{'Face': {'BoundingBox': {'Height': 0.45614033937454224,
#      'Left': 0.25925925374031067,
#      'Top': 0.06578947603702545,
#      'Width': 0.2567901313304901},
#     'Confidence': 99.99740600585938,
#     'Landmarks': [{'Type': 'eyeLeft',
#       'X': 0.3468391001224518,
#       'Y': 0.26327452063560486},
#      {'Type': 'eyeRight', 'X': 0.430842787027359, 'Y': 0.255566269159317},
#      {'Type': 'nose', 'X': 0.3944968283176422, 'Y': 0.3450881540775299},
#      {'Type': 'mouthLeft', 'X': 0.3547839820384979, 'Y': 0.4061143398284912},
#      {'Type': 'mouthRight',
#       'X': 0.4283067584037781,
#       'Y': 0.40353700518608093}],
#     'Pose': {'Pitch': -5.742334365844727,
#      'Roll': -3.6629204750061035,
#      'Yaw': 4.655891418457031},
#     'Quality': {'Brightness': 56.744651794433594,
#      'Sharpness': 99.95819854736328}},
#    'Id': '1SK7cR8M',
#    'MatchConfidence': 100.0,
#    'Name': 'Jeff Bezos',
#    'Urls': ['www.imdb.com/name/nm1757263']}],
#  'OrientationCorrection': 'ROTATE_0',
#  'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
#    'content-length': '847',
#    'content-type': 'application/x-amz-json-1.1',
#    'date': 'Thu, 02 Aug 2018 22:17:38 GMT',
#    'x-amzn-requestid': 'dd259a44-96a1-11e8-9943-9d73667d5b20'},
#   'HTTPStatusCode': 200,
#   'RequestId': 'dd259a44-96a1-11e8-9943-9d73667d5b20',
#   'RetryAttempts': 0},
#  'UnrecognizedFaces': []}
