#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Root route
@app.route('/')
def index():
    return make_response(jsonify({"message": "Welcome to the Plant API!"}), 200)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = [plant.to_dict() for plant in plants]
        return make_response(jsonify(plant_list), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price")
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return make_response(jsonify(plant.to_dict()), 200)

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
