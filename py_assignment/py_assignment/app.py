#!flask /bin/python
from flask import Flask,jsonify,request
from controller.main import main

app = Flask(__name__)
app.register_blueprint(main)

@app.route('/')
def home():
    return 'Welcome To The Api Developed By Suraj Bhatt'
