from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields
import bcrypt
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URL
db = SQLAlchemy(app)
api = Api(app, version='1.0', title='Your API', description='API description')

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
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
        }
        token = jwt.encode(token_payload, 'your_secret_key', algorithm='HS256')

        return {'access_token': token.decode('utf-8')}, 200

# Protected route that requires authentication
@app.route('/protected')
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
    db.create_all()
    app.run(debug=True)
