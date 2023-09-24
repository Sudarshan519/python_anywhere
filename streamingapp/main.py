import jwt
from datetime import datetime,timedelta
import bcrypt
from flask import Flask, request,g
from flask_restx import Api, Resource, fields,reqparse
from flask_serialize import FlaskSerialize
from werkzeug.datastructures import FileStorage
import os
from flask_sqlalchemy import SQLAlchemy
# from . import db
# Configure the "media" directory path
MEDIA_DIRECTORY = 'media'

# Ensure the "media" directory exists
if not os.path.exists(MEDIA_DIRECTORY):
    os.makedirs(MEDIA_DIRECTORY)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# api = Api(app, version='1.0', title='File Upload API', description='API for uploading files')
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300  # For example, set to 30 seconds
#db=SQLAlchey(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'example.db')

db = SQLAlchemy(app)
fs_mixin = FlaskSerialize(db)
api = Api(app, version='1.0', title='Streaming ', description='API for managing multiple models with file upload')

ns = api.namespace('', description='Carousels')

# upload_parser = ns.parser()
# upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Upload a file')
# Define a generic model using Flask-RESTx fields
carousel_model = api.model('CarouselModel', {
    'id': fields.Integer(readonly=True, description='Unique identifier'),
    'name': fields.String(required=True, description='Item name'),
    'description': fields.String(description='Item description'),
    'logo': fields.String(description='Uploaded file path')
})

# # Define another model with a different structure
# movie_model = api.model('MovieModel', {
#     'id': fields.Integer(readonly=True, description='Unique identifier'),
#     'title': fields.String(required=True, description='Item title'),
#     'description': fields.String(description='Item content'),
#     'movie': fields.String(description='Uploaded file path')
# })
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_superuser=db.Column(db.Boolean,default=False)
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


class CarouselModel(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'logo': self.logo
        }
class MovieModel(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    movie=db.Column(db.String(255))
    trailer=db.Column(db.String(255))
    genre=db.Column(db.String(255))
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'logo': self.logo,
            'genre':self.genre,
            'movie':self.movie,
            'trailer':self.trailer
        }
movie_upload_parser = reqparse.RequestParser()

movie_upload_parser.add_argument('name', type=str, required=True, help='Item name is required')
movie_upload_parser.add_argument('description', type=str, help='Item description')
movie_upload_parser.add_argument('movie', type=FileStorage, location='files', required=True, help='File upload')
movie_upload_parser.add_argument('logo', type=FileStorage, location='files', required=True, help='File upload')
movie_upload_parser.add_argument('trailer', type=str,  help='Youtube trailer id')
movie_upload_parser.add_argument('genre', type=str,  help='Youtube trailer id')



class Tvshow(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255)) 
    trailer=db.Column(db.String(255))
class Episode(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define a foreign key relationship to the User table
    tv_show_id = db.Column(db.Integer, db.ForeignKey('tvshow.id'), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    episode=db.Column(db.String(255))
    trailer=db.Column(db.String(255))

class SubscriponPlan(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)

class UserPlan(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id=db.Column(db.Integer,db.ForeignKey("payment.id"))
class Payment(fs_mixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Float)
    type=db.Column(db.String(256))
generic_upload_parser = reqparse.RequestParser()

generic_upload_parser.add_argument('name', type=str, required=True, help='Item name is required')
generic_upload_parser.add_argument('description', type=str, help='Item description')
generic_upload_parser.add_argument('file', type=FileStorage, location='files', required=True, help='File upload')


another_upload_parser = reqparse.RequestParser()
another_upload_parser.add_argument('file', type=FileStorage, location='files')
# Register teardown function to close database session
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


class GenericResource(Resource):

    # def __init__(self):
    #     super().__init__()
 
        # self.model = model
    #     self.api_model = api_model
    #     self.upload_parser = upload_parser

    def get(self, item_id):
        item = self.model.fs_get_delete_put_post(item_id)
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
        print(self.model)
        # item = self.model.query.get(item_id)
        # if item is None:
        #     api.abort(404, f"{self.model.__name__} not found")
        # db.session.delete(item)
        # db.session.commit()
        return None, 204
carousel = api.namespace('carousel', description='File Upload')

@app.route('/students', methods=['GET', 'POST'])
@carousel.doc(params={'item_id': 'The ID of the item'})#
def all_students(item_id=None):
    # students=CarouselModel.query.all()
    # return Item.fs_get_delete_put_post(item_id)
    return CarouselModel.fs_get_delete_put_post(item_id)


@app.route('/list/', methods=['GET'])
@api.doc(params={},tags=["Carousel"])
def get_setting_all():
    return CarouselModel.fs_get_delete_put_post()
@ns.route('/carousels')
@api.doc()
class ItemListResource(Resource):
    
    # @api.marshal_list_with(carousel_model)
    def get(self):
        return CarouselModel.fs_get_delete_put_post()
    
    @api.expect(generic_upload_parser)
    def post(self):
        args = generic_upload_parser.parse_args()
        uploaded_file = args['file']

        if uploaded_file:
            # Save the uploaded file
            file_path = os.path.join('media', uploaded_file.filename)
            uploaded_file.save(file_path)
            # item.file = file_path
            # Create a new item with file_path
            new_item = CarouselModel(
                name=args['name'],
                description=args['description'],
                logo=file_path
            )
            db.session.add(new_item)
            db.session.commit()
            return new_item.as_dict()
        else:
            api.abort(400, 'No file uploaded')


@ns.route('/carousels/<int:item_id>', endpoint='generic_item')#<int:item_id>
@api.doc(params={'item_id': 'The ID of the item'})#
class CarouselModelResource(Resource):
    model=CarouselModel
    def get(self, item_id=None):
        
        if item_id:
            item = self.model.fs_get_delete_put_post(item_id)
            if item is None:
                api.abort(404, f"{self.model.__name__} not found")
            return item
        
        

movie = api.namespace('movie', description='Movie')
@movie.route("/movie")
class MovieModelResource(Resource):
    model=MovieModel
    def get(self):
        return MovieModel.fs_get_delete_put_post()
    
    @api.expect(movie_upload_parser)
    def post(self):
        args = movie_upload_parser.parse_args()
        uploaded_file = args['movie']
        logo=args['logo']
        if logo:
            logo_path = os.path.join('media', uploaded_file.filename)
            uploaded_file.save(logo_path)
        if uploaded_file:
            # Save the uploaded file
            file_path = os.path.join('media', uploaded_file.filename)
            uploaded_file.save(file_path)
            
            # item.file = file_path
            # Create a new item with file_path
            new_item = MovieModel(
                name=args['name'],
                description=args['description'],
                logo=file_path,
                movie=logo_path,
                trailer=args['trailer']
            )
            db.session.add(new_item)
            db.session.commit()
            db.session.refresh(new_item)
            return new_item.as_dict()
        else:
            api.abort(400, 'No file uploaded')

@movie.route("/movie:<int:id>")
class MovieModelResource(Resource):
    model=MovieModel
    def get(self,id):
        return MovieModel.fs_get_delete_put_post(id)
@movie.route("/watch-movie:<int:id>")
class WatchMovieResource(Resource):

    model=MovieModel
  
    def get(self,id):
        return MovieModel.fs_get_delete_put_post(id)



# Register the User model with Flask-RESTPlus
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

 

# User registration endpoint
@api.route('/register')
class UserRegistration(Resource):
    @api.expect(user_model)
    def post(self):
        """Register a new user"""
        data = api.payload
        username = data['username']
        password = data['password']

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

# User login endpoint
@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_model)
    def post(self):
        """User login and token generation"""
        data = api.payload
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'message': 'Invalid username or password'}, 401

        # Generate a JWT token
        token_payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() +timedelta(days=1)  # Token expiration time
        }
        token = jwt.encode(token_payload, 'your_secret_key', algorithm='HS256')
        # print(jwt.decode(token))
        return {'access_token': token}, 200


def login_required(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        headers = request.headers
        print(headers)
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'message': 'Authorization header missing or invalid'}, 401

        token = auth_header.split(' ')[1]
        
        try:
            
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            user_id = payload['user_id']
            kwargs['user_id'] = user_id
            return func(*args, **kwargs)
            return {'message': 'This route is protected', 'user_id': user_id}, 200
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401

        return func(*args, **kwargs)
        print("Something is happening after the function is called.")
    return wrapper
# Define a model for the expected header
header_model = api.model('CustomHeader', {
    'Authorization': fields.String(description='Authorization token', required=True),
    'X-Custom-Header': fields.String(description='Custom header'),
})


# from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Protected route that requires authentication
parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('Authorization', location='headers')
@api.route("/hello")
@api.header('X-Header', 'Some class header')
@api.expect(parser)
# @api.expect(header_model, validate=True)
class Hello(Resource): 
    @login_required
    
    # @api.doc(params={'item_id': 'The ID of the item'})#
    # @jwt_required()
    # @api.expect(parser)
    def get(self,user_id):
        """
        Get resource
        
        ---
        responses:
          200:
            description: Resource fetched successfully
        parameters:
          - in: header
            name: Authorization
            schema:
              type: string
            description: Authorization token
          - in: header
            name: X-Custom-Header
            schema:
              type: string
            description: Custom header
        """
        return {'message': 'This route is protected', 'user_id': user_id}, 200
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'message': 'Authorization header missing or invalid'}, 401

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            user_id = payload['user_id']
            return {'message': 'This route is protected', 'user_id': user_id}, 200
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401



 
@app.route('/protected')
@api.expect(user_model)
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return {'message': 'Authorization header missing or invalid'}, 401

    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        user_id = payload['user_id']
        return {'message': 'This route is protected', 'user_id': user_id}, 200
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}, 401



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
