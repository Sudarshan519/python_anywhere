
# A very simple Flask Hello World app for you to get started with...

import sys
path = '/home/SudarshanShrestha/mysite'
if path not in sys.path:
   sys.path.insert(0, path)

from flask_app import app as application

@app.route('/')
def home():
    # etc etc, flask app code
    return {"response":"Hello  world"
if __name__ == '__main__':
    app.run()
