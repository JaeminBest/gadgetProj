# views.py
# author : jaemin kim
# details : front-end program that works as web page, implemented basic API

from flask import render_template, redirect, request, session, jsonify, url_for

# connecting DB
from app import app, engine, db_session
from database import db_session, engine
from models import User, Mark, Original
from sqlalchemy.sql import text
from sqlalchemy import update


from flask_wtf import FlaskForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin_man():
    return render_template("admin.html")

# /request_checking : show all user DB
@app.route('/admin/request_checking', methods = ['GET','POST'])
def request_checking():
    req = request.get_json()
    if request.method == 'GET' or request.method == 'POST' :
        return f'{req}'
    else:
        return "appropriate request has not received"

def check_db(user_id):
    #query database to pass object to the callback
    db_check = User.query.get(user_id)
    UserObject = User(username=db_check['username'], email=db_check['email'], password=db_check['password'])
    if UserObject.id == user_id:
        return UserObject
    else:
        return None

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return check_db(id)

# /login : login to account
@app.route('/admin/login', methods = ['GET', 'POST'])
def login():
    db_session.expire_all()
    res = {}
    req = request.get_json()
    if request.method == "POST":
        if ("username" in req) and ("password" in req):
            #username_1 = req['username']
            #password_1 = req['password']
            # return user_name
            sql = """
            SELECT user.user_id AS id, user.username AS username, user.email AS email, user.password AS password, user.deleted AS deleted
            FROM user
            WHERE user.username = :username_1
            AND user.password = :password_1
            """
            param = {'username_1' : req['username'], 'password_1' : req['password']}
            users = engine.execute(text(sql), param).fetchall()

            if users is None:
                return "User is not registered. Check your username or password."
            else:
                for user in users:
                    res[f"'{user.id}'"] = user
                    return f"'{res}''"
        else:
            return 'Please enter username and password'
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # return redirect(url_for('next')) #this code is completed when the next url on the react frontend is established


# /show_all_user : show all user DB
@app.route('/admin/show_all_user')
def show_all_user():
    res = {}
    users = User.query.all()
    for user in users:
        res[f"'{user.id}'"] = user
    return f"'{res}'"

# /show_all_edit : show all edit DB
@app.route('/admin/show_all_edit')
def show_all_edit():
    res = {}
    marks = Mark.query.all()
    for mark in marks:
        res[f"'{mark.id}'"] = mark
    return f"'{res}'"

# /show_one_user : show one user by user_id
@app.route('/admin/show_one_user', methods=['GET'])
def show_one_user():
    user_id = request.args.get('id', default = '0', type = str)
    db_session.expire_all()
    req = request.get_json()
    res = {}
    if request.method == 'GET':
        if user_id != '0':
            user_temp = User.query.filter(User.id==user_id).first()

            if user_temp is not None:
                if user_temp.deleted:
                    return "no longer exist"
                else:
                    res['user_id'] = user_temp.id
                    res['user_username'] = user_temp.username
                    res['user_email'] = user_temp.email
                    res['user_password'] = user_temp.password
                    return jsonify(res)
            else:
                return "no user found"
        else:
            return "Bad request, request should be json object that include key of 'user_id'"
    return "(show_one_user)No request received, request should be GET method"


# /test_register : register one user by username, email, password and show all list of user DB
@app.route('/admin/test_register',methods = ['POST'])
def test_register():
    req = request.get_json()
    res = {}
    if request.method == 'POST':
        if ("username" in req) and ("email" in req) and ("password" in req):
            user_temp = User.query.filter(User.username==req["username"])
            if not user_temp == []:
                for user in user_temp:
                    if not user.deleted:
                        return f"'{user_temp}'existing username!"

            user_temp = User.query.filter(User.username==req["email"])
            if not user_temp == []:
                for user in user_temp:
                    if not user.deleted:
                        return f"'{user_temp}'existing email!"


            user_temp = User(username=req["username"], email=req["email"], password=req["password"])

            try:
                db_session.add(user_temp)
                db_session.commit()
            except:
                db_session.rollback()
                return "commit failed, failure in system!"
            return redirect(url_for('show_all_user'))
        else:
            return "Bad request, request should be json object that include key of 'username','email','password'"
    return "(test_register)No request received, request should be POST method"


# /test_unregister : unregister one user by user_id
@app.route('/admin/test_unregister', methods=['GET'])
def test_unregister():
    req = request.get_json()
    res = {}
    if request.method == 'GET':
        if 'user_id' in req:
            user_temp = User.query.filter(User.id==req["user_id"]).first()
            if not user_temp == None:
                if not user_temp.deleted:
                    stmt = update(users).where(users.c.id==req["user_id"]).\
                            values(deleted=True)
                    try:
                        db_session.commit()
                    except:
                        db_session.rollback()
                        return "commit failed, failure in system!"
                    return redirect(url_for('show_all_user'))
            else:
                return "No user having this user_id"
        else:
            return "Bad request, request should be json object that include key of 'user_id'"
    return "(test_unregister)No request received, request should be GET method"

# /show_one_image : show one original image by id(only detail)
@app.route('/admin/show_one_image', methods=['GET'])
def show_one_image():
    org_id = request.args.get('id', default = '0', type = str)
    db_session.expire_all()
    res = {}
    if request.method == 'GET':
        if org_id != '0':
            org_temp = Original.query.filter(Original.id==org_id).first()

            if not org_temp == None:
                res['id'] = org_temp.id
                res['image_code'] = org_temp.image_code
                res['part_num'] = org_temp.part_num
                res['label_num'] = org_temp.label_num

                photo_encoded = b64encode(org_temp.data)
                photo_decoded = photo_encoded.decode('utf-8')
                res['photo'] = photo_decoded

                pixel = [(905,14),(1389,77),(1584,22),(2702,162),(4267,249),(5278,161)]

                res['pixel_x'] = pixel[res['label_num']][0]
                res['pixel_y'] = pixel[res['label_num']][1]

                return jsonify(res)
            else:
                return "no original image found"
        else:
            return "Bad request, request should be json object that include key of 'id'"
    return "(show_one_image)No request received, request should be GET method"

# /show_one_edit : show one edited image by edit_id(only detail)
@app.route('/admin/show_one_edit', methods=['GET'])
def show_one_edit():
    edit_id = request.args.get('id', default = '0', type = str)
    db_session.expire_all()
    res = {}
    if request.method == 'GET':
        if edit_id != '0':
            edit_temp = Mark.query.filter(Mark.id==edit_id).first()
            if not edit_temp == None:
                db_session.refresh(edit_temp)
                res['id'] = edit_temp.id
                res['user_id'] = edit_temp.user_id
                res['image_id'] = edit_temp.org_id
                res['date_edited'] = edit_temp.date_edited
                res['deleted'] = edit_temp.deleted
                photo_encoded = b64encode(edit_temp.data)
                photo_decoded = photo_encoded.decode('utf-8')
                res['photo'] = photo_decoded
                return jsonify(res)
            else:
                return "no edited image found"
        else:
            return "Bad request, request should be json object that include key of 'id'"
    return "(show_edited_image)No request received, request should be GET method"

# /save_edited_image : post the edited image to EDIT db given edited photo, user_id, org_id
@app.route('/admin/save_edited_image', methods=['POST'])
def save_edited_image():
    # db_session.expire_all()
    req = request.get_json()

    if request.method == 'POST':
        # if ("user_id" in req) and ("org_id" in req) and ("photo" in req):
        if ("user_id" in req) and ("org_id" in req) and ("photo" in req) and ("date_edited" in req):
            # assume photo is in string base64 form. we need to change to longblob form
            photo_decoded = b64decode(req['photo'])
            edited = Mark(user_id=req['user_id'], org_id=req['org_id'], data=photo_decoded)
            db_session.add(edited)
            try:
                db_session.commit()
            except:
                db_session.rollback()
                return "commit failed, failure in system!"
            return redirect(url_for('show_all_edit'))
        else:
            return "Bad request, request should be json object that inclue key of 'user_id', 'org_id', 'photo', 'date'!"
    else:
        return f"(save_edited_image)No request received, request should be POST method"


@app.route('/admin/delete_edited_image', methods=['GET'])
def delete_edited_image():
    req = request.get_json()
    # res = {}
    if request.method == 'GET':
        if 'edit_id' in req:
            edit_temp = Mark.query.filter(Mark.id==edit_id).first()
            if not edit_temp == None:
                if not edit_temp.deleted:
                    stmt = update(marks).where(marks.c.id==req["edit_id"]).\
                            values(deleted=True)
                    try:
                        db_session.commit()
                    except:
                        db_session.rollback()
                        return "commit failed, failure in system!"
                    return redirect(url_for('show_all_edit'))
            else:
                return "No edited image having this edit_id"
        else:
            return "Bad request, request should be json object that include key of 'edit_id'"
    else:
        return "(delete_edited_image)No request received, request should be GET method"


# /display_image : display original image by id
@app.route('/admin/display_image', methods=['GET'])
def test_diplay_image():
    db_session.expire_all()
    req = request.get_json()
    res = {}
    if request.method == 'GET':
        if "org_id" in req:
            org_temp = Original.query.filter(Original.id==org_id).first()
            res = b64encode(org_temp.data)
            return render_template("show.html",res=res)
        else:
            return "Bad request, request should be json object that include key of 'id'"
    return "(test_display_image)No request received, request should be GET method"
