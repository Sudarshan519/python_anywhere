from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
api = Api(app, version='1.0', title='Generic CRUD API', description='API for managing generic models')

# Define a generic model using Flask-RESTx fields
generic_model = api.model('GenericModel', {
    'id': fields.Integer(readonly=True, description='Unique identifier'),
    'name': fields.String(required=True, description='Item name'),
    'description': fields.String(description='Item description'),
})

class GenericItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

# db.create_all()

class GenericResource(Resource):
    def __init__(self, model, api_model):
        self.model = model
        self.api_model = api_model
    def get(self, item_id):
        item = self.model.query.get(item_id)
        if item is None:
            api.abort(404, f"{self.model.__name__} not found")
        return item

    def put(self, item_id):
        item = self.model.query.get(item_id)
        if item is None:
            api.abort(404, f"{self.model.__name__} not found")

        updated_item_data = api.payload
        for key, value in updated_item_data.items():
            setattr(item, key, value)
        db.session.commit()
        return item

    def delete(self, item_id):
        item = self.model.query.get(item_id)
        if item is None:
            api.abort(404, f"{self.model.__name__} not found")
        db.session.delete(item)
        db.session.commit()
        return None, 204

# Create a resource for managing GenericItem
api.add_resource(GenericResource, '/generic/<int:item_id>', resource_class_kwargs={'model': GenericItem, 'api_model': generic_model})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
