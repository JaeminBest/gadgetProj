# views.py
# author : jaemin kim
# details : front-end program that works as web page, implemented basic API

from flask import render_template, redirect, request, session, jsonify, url_for

# connecting DB
from app import app, db, engine
from app.models import User, Edit, Original
from sqlalchemy.sql import text

# for all form of flask, rendering field ...etc
from flask_wtf import FlaskForm

# for sign-in and sign-up form
#from wtforms import StringField, PasswordField, BooleanField, Form, validators
#from wtforms.validators import InputRequired, Email, Length
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# for test display image
from base64 import b64encode, b64decode

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
    db.session.expire_all()
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
    sql = """
    SELECT user.user_id AS id, user.username AS username, user.email AS email, user.password AS password, user.deleted AS deleted
    FROM user
    WHERE user.deleted = false
    """
    users = engine.execute(text(sql)).fetchall()
    for user in users:
        res[f"'{user.id}'"] = user
    return f"'{res}'"

# /show_all_edit : show all edit DB
@app.route('/admin/show_all_edit')
def show_all_edit():
    res = {}
    sql = """
    SELECT edit.edit_id AS id, edit.user_id AS user_id, edit.org_id AS org_id, edit.date_edited AS date_edited, edit.deleted AS deleted
    FROM edit
    WHERE edit.deleted = false
    """
    edits = engine.execute(text(sql)).fetchall()
    for edit in edits:
        res[f"'{edit.id}'"] = edit
    return f"'{res}'"

# /show_one_user : show one user by user_id
@app.route('/admin/show_one_user', methods=['GET'])
def show_one_user():
    user_id = request.args.get('id', default = '0', type = str)
    db.session.expire_all()
    req = request.get_json()
    res = {}
    if request.method == 'GET':
        if user_id != '0':
            sql1 = """
            SELECT user.user_id AS id, user.username AS username, user.email AS email, user.password AS password, user.deleted AS deleted
            FROM user
            WHERE user.user_id = :param_1
            """
            user_temp = engine.execute(text(sql1), {'param_1':user_id}).fetchall()

            sql2 = """
            SELECT edit.edit_id AS edit_edit_id, edit.photo AS edit_photo, edit.user_id AS edit_user_id, edit.org_id AS edit_org_id, edit.deleted AS edit_deleted, edit.mark_id AS edit_mark_id, edit.date_edited AS edit_date_edited
            FROM edit
            WHERE edit.user_id = :param_2
            """
            history = engine.execute(text(sql2), {'param_2': user_id}).fetchall()

            if not user_temp == []:
                user_temp = user_temp[0]
                if user_temp.deleted:
                    return "no longer exist"
                else:
                    res['user_id'] = user_temp.id
                    res['user_username'] = user_temp.username
                    res['user_email'] = user_temp.email
                    res['user_password'] = user_temp.password
                    res['user_history'] = history
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

            sql1 = """
            SELECT user.user_id AS id, user.username AS username, user.email AS email, user.password AS password, user.deleted AS deleted
            FROM user
            WHERE user.username = :username_1
            """
            user_temp = engine.execute(text(sql1), {'username_1': req["username"]}).fetchall()
            if not user_temp == []:
                for user in user_temp:
                    if not user.deleted:
                        return f"'{user_temp}'existing username!"

            sql2 = """
            SELECT user.user_id AS id, user.username AS username, user.email AS email, user.password AS password, user.deleted AS deleted
            FROM user
            WHERE user.email = :email_1
            """
            user_temp = engine.execute(text(sql2), {'email_1': req["email"]}).fetchall()
            if not user_temp == []:
                for user in user_temp:
                    if not user.deleted:
                        return f"'{user_temp}'existing email!"

            sql3 = """
            INSERT INTO user (username, email, password, deleted) VALUES (:username, :email, :password, :deleted)
            """
            param = {'username' : req['username'], 'email' : req['email'], 'password' : req['password'], 'deleted' : False}
            engine.execute(text(sql3), param)
            try:
                connection = engine.connect()
                trans = connection.begin()
                trans.commit()
            except:
                trans.rollback()
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
            sql1 = """
            SELECT user.user_id AS id, user.username AS username, user.email AS email, user.password AS password, user.deleted AS deleted
            FROM user
            WHERE user.user_id = :param_1
            """
            user_temp = engine.execute(text(sql1), {'param_1': req['user_id']}).fetchone()
            if not user_temp == None:
                if not user_temp.deleted:
                    sql2 = """
                    UPDATE user
                    SET deleted=:deleted
                    WHERE user.user_id = :user_id
                    """
                    param = {'deleted' : True,'user_id' : req['user_id']}
                    engine.execute(text(sql2), param)
                    try:
                        connection = engine.connect()
                        trans = connection.begin()
                        trans.commit()
                    except:
                        trans.rollback()
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
    db.session.expire_all()
    res = {}
    if request.method == 'GET':
        if org_id != '0':
            sql1 = """
            SELECT original.org_id AS id,
            original.path AS path,
            original.image_code AS image_code,
            original.seg_num AS seg_num,
            original.part_num AS part_num,
            original.mark_num AS mark_num,
            original.collection_num AS collection_num,
            original.photo AS photo
            FROM original
            WHERE original.org_id = :param_1
            """
            org_temp = engine.execute(text(sql1), {'param_1': org_id}).fetchone()
            if not org_temp == None:
                res['id'] = org_temp.id
                res['path'] = org_temp.path
                res['image_code'] = org_temp.image_code
                res['seg_num'] = org_temp.seg_num
                res['part_num'] = org_temp.part_num
                res['mark_num'] = org_temp.mark_num
                res['collection_num'] = org_temp.collection_num

                photo_encoded = b64encode(org_temp.photo)
                photo_decoded = photo_encoded.decode('utf-8')
                res['photo'] = photo_decoded

                pixel = [(905,14),(1389,77),(1584,22),(2702,162),(4267,249),(5278,161)]

                res['pixel_x'] = pixel[res['part_num']][0]
                res['pixel_y'] = pixel[res['part_num']][1]

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
    db.session.expire_all()
    res = {}
    if request.method == 'GET':
        if edit_id != '0':
            edit_temp = db.session.query(Edit).get(edit_id)
            if not edit_temp == None:
                db.session.refresh(edit_temp)
                res['id'] = edit_temp.id
                res['user_id'] = edit_temp.user_id
                res['image_id'] = edit_temp.org_id
                res['mark_id'] = edit_temp.mark_id
                res['date_edited'] = edit_temp.date_edited
                res['deleted'] = edit_temp.deleted

                photo_encoded = b64encode(edit_temp.photo)
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
    # db.session.expire_all()
    req = request.get_json()
    
    if request.method == 'POST':
        # if ("user_id" in req) and ("org_id" in req) and ("photo" in req):
        if ("user_id" in req) and ("org_id" in req) and ("photo" in req) and ("date_edited" in req):
            # assume photo is in string base64 form. we need to change to longblob form
            photo_decoded = b64decode(req['photo'])

            edited = Edit(user_id=req['user_id'], org_id=req['org_id'], photo=photo_decoded, date_edited=req['date_edited'])


            db.session.add(edited)
            db.session.commit()
            db.session.refresh(edited)
            # edited_id = edited.id
            # edited.set

            #edit_obj=db.session.query(Edit).get(edited.id)
            sql1 = '''
            UPDATE edit
            SET mark_id = mark_id + 1
            WHERE edit.edit_id = :edit_id
            '''
            param1 = {'edit_id' : edited.id}
            engine.execute(text(sql1), param1)

            sql2 = '''
            UPDATE original
            SET mark_num = mark_num + 1
            WHERE original.org_id = :org_id
            '''
            param2 = {'org_id' : req['org_id']}
            engine.execute(text(sql2), param2)

            try:
                connection = engine.connect()
                trans = connection.begin()
                trans.commit()
            except:
                trans.rollback()
                return "commit failed, failure in system!"
            
            # edit_obj.set()

            #return f"'{edit_obj.mark_id}'"
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
            sql1 = """
            SELECT edit.edit_id AS id, edit.user_id AS user_id, edit.org_id AS org_id, edit.deleted AS deleted
            FROM edit
            WHERE edit.edit_id = :param_1
            """
            edit_temp = engine.execute(text(sql1), {'param_1': req['edit_id']}).fetchone()
            if not edit_temp == None:
                if not edit_temp.deleted:
                    sql2 = """
                    UPDATE edit
                    SET deleted=:deleted
                    WHERE edit.edit_id = :edit_id
                    """
                    param = {'deleted' : True,'edit_id' : req['edit_id']}
                    engine.execute(text(sql2), param)
                    
                    return f"'{param}'"

                    # try:
                    #     connection = engine.connect()
                    #     trans = connection.begin()
                    #     trans.commit()
                    # except:
                    #     trans.rollback()
                    #     return "commit failed, failure in system!"
                    # return redirect(url_for('show_all_edit'))
            else:
                return "No edited image having this edit_id"
        else:
            return "Bad request, request should be json object that include key of 'edit_id'"
    else:
        return "(delete_edited_image)No request received, request should be GET method"


# /display_image : display original image by id
@app.route('/admin/display_image', methods=['GET'])
def test_diplay_image():
    db.session.expire_all()
    req = request.get_json()
    res = {}
    if request.method == 'GET':
        if "org_id" in req:
            org_temp = db.session.query(Original).get(req['org_id'])
            res = b64encode(org_temp.photo)
            return render_template("show.html",res=res)
        else:
            return "Bad request, request should be json object that include key of 'id'"
    return "(test_display_image)No request received, request should be GET method"
