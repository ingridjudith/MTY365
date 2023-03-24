from flask import Flask, jsonify, request, render_template,request, redirect, url_for
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId
import json

app = Flask(__name__)

client = MongoClient('mongodb+srv://a01177640:Oc0AMR2QKYeXgFOq@mty365.154j6qb.mongodb.net/?retryWrites=true&w=majority', 
                        tls=True,
                        tlsAllowInvalidCertificates=True)
db = client.Mty365
collection = db.spots


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/form')
def form():
	return render_template('form.html')



@app.route('/add_spot', methods=['POST'])
def add_spot():
    spotInfo = request.get_json()  # Assumes the request contains a JSON payload with the new document data
    new_spot = {
        'title': spotInfo['title'],
        'author': spotInfo['author'],
        'location': spotInfo['location'],
        'category': spotInfo['category'],
        'image': spotInfo['image'],
        'description': spotInfo['description'],
    }
    result = collection.insert_one(new_spot)
    return f"Inserted document with ID {result.inserted_id}"

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        print("Failed to serialize object:", o)
        return json.JSONEncoder.default(self, o)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/spots', methods=['GET'])
def get_spots():
    spots = collection.find()
    response = {"spots": json.dumps(list(spots), cls=JSONEncoder)}
    return jsonify(response)

if __name__ == '__main__':
    app.run()