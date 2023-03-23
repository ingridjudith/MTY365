from flask import Flask, render_template,request,redirect,url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__)


client = MongoClient('mongodb+srv://a01177640:Oc0AMR2QKYeXgFOq@mty365.154j6qb.mongodb.net/?retryWrites=true&w=majority')
db = client['Mty365db']
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



'''
@app.route('/create')
def create_spots():
    spots_data = {
        'title': 'Artefacto',
        'author': 'John Doe',
        'location': 'https://goo.gl/maps/AXBN6ZR1zgqvHtyNA',
        'category': 'Convivencia',
        'image': 'https://i.imgur.com/5S8W7VJ.jpeg',
        'description': 'Dinámica: escoges una pieza de cerámica, la pintas y se hornea @__artefacto',
    }
    result = collection.insert_one(spots_data)
    return f'Inserted user with ID {result.inserted_id}'
'''
@app.route('/spots')
def get_spots():
    spotsList = collection.find()
    return str(spotsList)

if __name__ == '__main__':
    app.run()



'''


client = pymongo.MongoClient("mongodb+srv://<username>:<password>@mty365.154j6qb.mongodb.net/?retryWrites=true&w=majority")
db = client['MTY365db']
spots = db.spots

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)


@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

'''
