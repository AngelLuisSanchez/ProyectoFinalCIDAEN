
import boto3
import os
import time

s3 = boto3.client('s3')

s3bucket = os.environ['S3_BUCKET']

def move_to_s3_folder(directorio):
    
    listimagen = os.listdir('/tmp/'+ directorio + '/')

    for imagen in listimagen:
        i = open('/tmp/' + directorio + '/' + imagen, 'rb')
        response = s3.put_object(Body=i, Bucket=s3bucket, Key=directorio + '/' + imagen)
        print(response)
        i.close()
        time.sleep(10)

def get_url(key):
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': s3bucket,
            'Key': key
        }
    )

    return url
