from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt



def setup():
    app = Flask(__name__)

    return app