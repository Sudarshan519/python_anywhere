from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_restplus import Api, Resource

app = Flask(__name__)
app.secret_key = 'your_secret_key'

api = Api(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# User model for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'user_id': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['POST'])
def login(request):
    user_id = request.json.get('user_id')
    password = request.json.get('password')
    if users.get(user_id) and users[user_id]['password'] == password:
        user = User(user_id)
        login_user(user)
        return {'message': 'Logged in successfully'}, 200
    return {'message': 'Invalid credentials'}, 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return {'message': 'Logged out successfully'}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @login_required
    def get(self):
        return {'message': 'Protected Route'}

if __name__ == '__main__':
    app.run()
