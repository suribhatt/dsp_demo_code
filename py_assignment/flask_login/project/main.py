from flask import Flask,Blueprint,jsonify,request
from .model import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required,current_user,logout_user

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return 'Api Created By Deepak Gusain For Scry Analytics'



@main.route('/profile')
@login_required
def profile():
    return  "Current User Name Is%s"%current_user.name

@main.route('/signin',methods=['POST'])
def signin():
    status = False
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            print("=============name",user.name)
            login_user(user)
            status = True
            response = {'message':'SuccessFully Login','id':user.id}
        else:
            response = 'Invalid Login Details, So kindly check the login details'
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})

@main.route('/signup', methods=['POST'])
def signup():
    status = False
    try:
        data = request.get_json()
        print("==================",data)
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            response = 'User is alredy present'
        else:
            user = User(name=name,password=generate_password_hash(password),email=email)
            if user:
                db.session.add(user)
                db.session.commit()
                status = True
                response = {'message':'User Create SuccessFully','id':user.id}
    except Exception as e:
        response = str(e)
    return jsonify({'status':status,'response':response})

@main.route('/logout')
@login_required
def logout():
    string = "Logout User Name Is %s"%current_user.name
    logout_user()
    return string