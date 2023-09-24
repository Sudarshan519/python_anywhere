from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API', description='A sample API', validate=True)

# Define a namespace for your API
ns = api.namespace('sample', description='Sample operations')

# Define a data model for your API
model = api.model('SampleModel', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='Name of the item')
})

# Create a list to hold sample data (replace this with your actual data source)
sample_data = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'},
]

# Create a simple resource for your API
@ns.route('/items')
class ItemList(Resource):
    @ns.doc('list_items')
    @ns.marshal_list_with(model)
    def get(self):
        """List all items"""
        return sample_data

if __name__ == '__main__':
    app.run(debug=True)
