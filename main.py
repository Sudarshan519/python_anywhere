# main.py
from flask import Flask, render_template, request
from flask import Blueprint, request
from blueprints.basic_endpoints import blueprint as basic_endpoints
from blueprints.jinja_endpoint import blueprint as jinja_template_blueprint

app = Flask(__name__)
app.register_blueprint(jinja_template_blueprint)
app.register_blueprint(basic_endpoints)
@app.route('/basic_api/hello_world')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def index():
    return render_template('portfolio.html')
if __name__ == "__main__":
    app.run(debug=True)