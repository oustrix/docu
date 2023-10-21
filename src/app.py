from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client['db']
objects = db['objects']


@app.route('/<key>', methods=['GET', 'POST', 'PUT'])
def index(key):
    if request.method == 'POST':
        data = request.get_json()
        if data:
            entry = {'key': key, 'data': data}
            result = objects.insert_one(entry)
            return jsonify({'message': 'Object was created', 'id': str(result.inserted_id)}), 201
        else:
            return jsonify({'error': 'Incorrect data'}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        if data:
            result = objects.update_one({'key': key}, {'$set': {'data': data}})
            if result.modified_count > 0:
                return jsonify({'message': 'Object was updated'}), 200
            else:
                return jsonify({'error': 'Not found'}), 404
        else:
            return jsonify({'error': 'Incorrect data'}), 400

    elif request.method == 'GET':
        entry = objects.find_one({'key': key})
        if entry:
            return jsonify({'key': entry['key'], 'data': entry['data']}), 200
        else:
            return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
