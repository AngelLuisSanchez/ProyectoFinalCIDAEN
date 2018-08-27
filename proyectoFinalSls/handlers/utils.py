import json
import datetime
import decimal
import random

from classes import Celebrities
from classes import WordCloud

#Return json data
def jsonify(obj):
    return {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'statusCode': 200,
        'body': json.dumps(obj)
    }

#Check if image contains people
def check_for_people(labels):
    names = ['Human', 'People', 'Person', 'Face']

    for label in labels:
        if(label['Name'] in names):
            return True
    
    return False

#Parse and return results from API objects and scenes
def parse_results_objects_and_scenes(response, label):
    try:
        if((label in response) and (len(response[label]) != 0)):
            return response[label]
        else:
            return {}
    except:
        print('No hay labels')
        return {}

#Return current date (month and year) that represents dynamodb key
def get_current_date():
    day = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%m")
    year = datetime.datetime.now().strftime("%Y")
    return str(day)+str(month)+str(year)

#Parse and return data of object and scenes
def parse_data_objects_and_scenes(labels_object):
    data = []
    for label in labels_object:
        data.append(
            {
                'Name': label['Name'],
                'Confidence': decimal.Decimal(str(label['Confidence']))
            }
        )
    return data

#Parse and return data of celebrities 
def parse_data_celebrities(labels_celebrities):
    data = []
    for label in labels_celebrities:
        url = 'Nulo'
        if('Urls' in label and len(label['Urls']) != 0):
            url = label['Urls'][0]
        data.append(
            {
                'Name': label['Name'],
                'Id': label['Id'],
                'Url': url
            }
        )
    return data

#Parse and return words of the cloud
def parse_data_cloud_tag(data):
    wordCloudTag = []
    l1 = []
    for r in data:
        if(len(r['Labels']) != 0):
            for l in r['Labels']:
                if l['Name'] not in l1:
                    l1.append(l['Name'])
                    wordCloudTag.append(
                        WordCloud.WordCloud(
                            l['Name'],
                            float(l['Confidence']),
                            generate_random_color()
                        )
                    )
    return wordCloudTag

#Return random color
def generate_random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

#Return parse list celebrities
def parse_list_celebrities(items):
    celebrities = []
    for item in items:
        if len(item['CelebrityFaces']) != 0:
            idImagen = item['idimagen']
            for celebrity in item['CelebrityFaces']:
                celebrities.append(
                    Celebrities.Celebrities(
                        celebrity['Id'],
                        celebrity['Name'],
                        celebrity['Url'],
                        idImagen
                    )
                )
    return celebrities

#Return parse date to search in dynamo
def parse_date(date):
    dateSplit = date.split('-')
    return dateSplit[2]+dateSplit[1]+dateSplit[0]

#Return count of celebrities
def countCelebrities(items):
    count = 0
    for item in items:
        count += len(item['CelebrityFaces'])
    return count
