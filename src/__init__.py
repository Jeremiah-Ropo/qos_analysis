from flask import Flask
# from firebase_admin import credentials, initialize_app
# from src.config import firebase_config

app = Flask(__name__)

# # Initialize Firebase Admin
# cred = credentials.Certificate(firebase_config)
# initialize_app(cred)

from .routes import *  # Import all routes into the app
