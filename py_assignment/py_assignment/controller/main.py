#!flask /bin/python
from flask import Flask,Blueprint,jsonify,request
import models
from models import hall_available,hall,professor


main = Blueprint('main', __name__, template_folder='templates')

@main.route('/add_hall',methods = ['POST'])
def add_hall():
    status = False
    try:
        obj_hall = hall.Hall()
        parameters = request.get_json()
        status,response = obj_hall.add_hall(parameters)
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})

@main.route('/add_professor',methods = ['POST'])
def add_professor():
    status = False
    try:
        obj_professor = professor.Professor()
        parameters = request.get_json()
        status,response = obj_professor.add_professor(parameters)
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})
    

@main.route('/get_hall_available',methods = ['GET'])
def get_hall_available():
    status = False
    try:
        obj_hall_available = hall_available.HallAvailable()
        parameters = request.get_json()
        status,response = obj_hall_available.get_hall_available(parameters)
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})


@main.route('/get_hall_data',methods = ['GET'])
def get_hall_data():
    status = False
    try:
        obj_hall_available = hall_available.HallAvailable()
        parameters = request.get_json()
        status,response = obj_hall_available.get_hall_data(parameters)
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})

@main.route('/add_hall_available',methods = ['POST'])
def add_hall_available():
    status = False
    try:
        obj_hall_available = hall_available.HallAvailable()
        parameters = request.get_json()
        status,response = obj_hall_available.add_hall_available(parameters)
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})

@main.route('/update_hall_available',methods = ['PUT'])
def update_hall_available():
    status = False
    try:
        obj_hall_available = hall_available.HallAvailable()
        parameters = request.get_json()
        status,response = obj_hall_available.update_hall_available(parameters)
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})