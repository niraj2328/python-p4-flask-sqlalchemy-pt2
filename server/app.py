#!/usr/bin/env python3

# server/app.py

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return make_response('<h1>Welcome to the pet/owner directory!</h1>', 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.get(id)

    if not pet:
        return make_response('<h1>404 pet not found</h1>', 404)

    response_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is {pet.species}</h2>
        <h2>Pet Owner is {pet.owner.name}</h2>
    '''

    return make_response(response_body, 200)

@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.get(id)

    if not owner:
        return make_response('<h1>404 owner not found</h1>', 404)

    response_body = f'<h1>Information for {owner.name}</h1>'

    pets = owner.pets.all()

    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
