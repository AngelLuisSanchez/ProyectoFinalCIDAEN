import json

def jsonify(obj):
    return {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'statusCode': 200,
        'body': json.dumps(obj)
    }
