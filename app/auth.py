from flask import Blueprint,request,jsonify,session
from .models import User
from .utils import Text_File_Handler
from pydantic import ValidationError
from functools import wraps


handler = Text_File_Handler("app/users.json")
auth = Blueprint('auth', __name__)

@auth.route("/signup",methods=['POST'])
def signup():
    try:
        req = request.get_json()
        user = User(**req) 
        print(user.username)
        usr = handler.get({"username":user.username})
        if(usr is not None ):
            return jsonify({"error":"User Exist"}),409
    except ValidationError as err:
        return jsonify({"errors":err.errors()}) ,400
    except Exception as exc:
        print(exc)
        return jsonify({"error":"Bad Request"}) ,400
    handler.add(user)

    return jsonify({"message":"User Succesfuly Created","data":user.model_dump_json()}) ,201
    



@auth.route("/login",methods=['POST'])
def login():
    try:
        req = request.get_json()
        user = User(**req) 
        print(user.username)
        usr = handler.get({"username":user.username})
        if(usr is  None ):
            return jsonify({"error":"User Not Exist"}),404
    except ValidationError as err:
        return jsonify({"errors":err.errors()}) ,400
    except Exception as exc:
        print(exc)
        return jsonify({"error":"Bad Request"}) ,400
    if(user.password == usr["password"]):
        session["user"] = user.username
        return jsonify({"message":"logged in Succesfuly ","data":user.model_dump_json()}) ,200
   
    
    return jsonify({"message":"Password or username not correct"}) ,400
    


@auth.route("/logout",methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message":"Logged Out"}),200


def login_required(f):
    @wraps(f)
    def wrapped_func(*args, **kwargs):
        username = session.get("user")
        if not username :
            return jsonify({"message":"Your Not Logged in"}),401
        return f(*args, **kwargs)
    return wrapped_func
    


