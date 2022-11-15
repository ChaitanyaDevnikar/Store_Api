from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import boto3, json

app = Flask(__name__)
stores = [
    {
        'name': 'Flower_store',
        'items': [
            {
                'name': 'Roses',
                'price': 100
            }
        ]
    },
    {
        'name': 'Books_store',
        'items': [
            {
                'name': 'Python Programming',
                'price': 100
            }
        ]
    }
]

app.json = LazyJSONEncoder


swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Swagger File for Our Store'),
    'version': LazyString(lambda: '0.1'),
    'description': LazyString(lambda: 'This document depicts a sample Swagger UI document and implements Store'
                                      'functionality after executing GET and POST methods'),
    },
    host = LazyString(lambda: request.host)
)


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'store',
            "route": '/store.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/storeapi/"
}

swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)
@swag_from("store.yml", methods=['GET','POST'])


@app.route('/')
def home():
    return "Welcome to Store_Api"


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>')
def get_store_name(name):
    for store in stores:
        if(store['name'] == name):
            return jsonify(store)
    return jsonify({'message': 'store not found'})


@app.route('/store')
def get_all_store_name():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_store_item(name):
    request_data = request.get_json()
    for store in stores:
        if(store['name'] == name):
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store not found'})


@app.route('/store/<string:name>/item')
def get_store_item(name):
    for store in stores:
        if(store['name'] == name):
            return jsonify(store['items'])
    return jsonify({'message': 'store not found'})

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Swagger File for Our Store'),
    'version': LazyString(lambda: '0.1'),
    'description': LazyString(lambda: 'This document depicts a sample Swagger UI document and implements Store'
                                      ' functionality after executing GET and POST methods'),
    },
    host = LazyString(lambda: request.host)
)




sqs = boto3.resource('sqs', region_name='ap-south-1')
queue = sqs.create_queue(QueueName='Storequeue', Attributes={'DelaySeconds': '10', 'VisibilityTimeout': '30'})
queue2 = sqs.get_queue_by_name(QueueName='Storequeue')
print(queue2.attributes)
response = queue.send_message(MessageBody='Hey, Welcome to the store')
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))
region_name = 'ap-south-1'
queue_name = 'Storequeue'
max_queue_messages = 10
message_bodies = []
aws_access_key_id = 'AKIA2PJN6IRF6EI4TEWL'
aws_secret_access_key = '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'
sqs = boto3.resource('sqs', region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
queue = sqs.get_queue_by_name(QueueName=queue_name)

app.run(port=5000)