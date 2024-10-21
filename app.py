from flask import Flask 

## Import the route handlers.
from src.routes import add_data, get_data, predict
from flask_cors import CORS

## Initialize the Flask app.
app = Flask(__name__)
CORS(app)

## Define the routes.
app.route('/qos_api/add_data', methods=['POST'])(add_data)
app.route('/qos_api/get_data', methods=['GET'])(get_data)
app.route('/qos_api/predict', methods=['POST'])(predict)

if __name__ == '__main__':
    app.run(debug=True)