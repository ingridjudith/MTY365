from flask import Flask, jsonify, request, render_template, request, redirect, url_for, Response
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

@app.route('/form', methods=['GET', 'POST'])
def cards():
    if request.method == 'POST':
        new_spot = {
        'title': request.form['nombre-lugar'],
        'author': request.form['autor'],
        'location': request.form['google-maps-url'],
        'category': request.form['categoria'],
        'image': request.form['image-url'],
        'description': request.form['descripcion'],
        }
        result = collection.insert_one(new_spot)
        print(result)

        return render_template('form.html')
    
    else:
        return render_template('form.html')


@app.route('/card', methods=['GET', 'POST'])
def form():
	return render_template('card.html')


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

@app.route('/get_spots', methods=['GET'])
def get_spots():
    spots = collection.find()
    response = {"spots": json.dumps(list(spots), cls=JSONEncoder)}
    return jsonify(response)


@app.route('/update_spot/<id>', methods= ['PATCH'])
def update_spot(id):
    
    title = request.form['title']
    author = request.form['author']
    location = request.form['location']
    category = request.form['category']
    image= request.form['image']
    description= request.form['description']
    try: 
        dbResponse = collection.update_one(
			{"_id": ObjectId(id)},
			{"$set": {'title': title, 
             'author': author,
             'location': location,
             'category': category,
             'image': image,
             'description': description
             }}
		)
        
        if dbResponse.modified_count == 1:
            return Response(
			response= json.dumps(
				{"message": "object updated"}),
				status= 200,
				mimetype= "application/json"
			)
            
    except Exception as ex:
        print("**")
        print(ex)
        print("**")
        
        return Response(
			response= json.dumps(
				{"message": "unable to update object"}),
			status=500,
			mimetype="application/json"
			)

@app.route("/delete_spot/<id>", methods = ["DELETE"])
def delete_spot(id):
    
    try: 
        dbResponse = collection.delete_one({"_id": ObjectId(id)})
        return Response(
			response= json.dumps(
				{"message": "user deleted", "id": f"{id}"}),
				status= 200,
				mimetype= "application/json"
			)
        
    except Exception as ex:
        print("**")
        print(ex)
        print("**")
        
        return Response(
			response= json.dumps(
				{"message": "unable to delete object"}),
			status=500,
			mimetype="application/json"
			)

if __name__ == '__main__':
    app.run()