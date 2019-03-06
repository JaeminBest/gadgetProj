# models.py
# author : jaemin kim
# details : back-end server DB model that describe user, original image, edits from users, and collection of edits that used for actual machine learning

from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGBLOB


# User DB which has columns of user id, username, email, password
# , DB of image that he(she) marked already
# neccessary input : id, username, email, password
# output : self.history
class User(db.Model):
    id = db.Column('user_id',db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False, default='default@email.com')
    password = db.Column(db.String(400), unique=False, nullable=False, default='0000')
    deleted = db.Column(db.Boolean, default=False)
    history = db.relationship('Edit',backref='editor', lazy=True)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password
        self.deleted = False

    def delete_user(self):
        if not self.deleted:
            self.deleted = True
            return True
        else:
            return False

    def __repr__(self):
        return f"User(id='{self.id}',username='{self.username}',email='{self.email}', deleted='{self.deleted}')"

# user has each repositry so that each edited image saved
# neccessary input : id(Edit id), img_file(info of saving img), user_id(user id), org_id(org. img id)
# metadata : org_path, mark_id(mark img id = marked num), mark_path, date_edited, editor, img
class Edit(db.Model):
    id = db.Column('edit_id', db.Integer, primary_key=True)

    # temporary file location of edited image file
    #img_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    photo = db.Column(LONGBLOB)   # in MySQL, it is BLOB type ---> if we save image itself to db??
    # FAILED : db.BLOB max_size is 65535 chars BUT size of our image is more than 355535 chars..

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) # decide by user
    org_id = db.Column(db.Integer, db.ForeignKey('original.org_id'), nullable=False) # decide by clicking specific original image
    # deleted = db.Column(db.Boolean, default=False)

    # image_path = db.Column(db.String(500)) # decide by clicking specific original image
    mark_id = db.Column(db.Integer, default=0 ) 
    #mark_path = db.Column(db.String(100), unique=True, default=f"{id}")
    date_edited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    # list of user that edit : self.editor
    # list of img that edit : self.img
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self,photo,user_id,org_id, date_edited):
        self.photo = photo
        self.user_id = user_id
        self.org_id = org_id
        self.date_edited = date_edited
        #self.date_edited = date_edited

    # MUST needed for basic setting of metadata
    def set(self):
        org_temp = Original.query.get(self.user_id)
        org_temp.mark_num += 1
        #self.image_path = org_temp.path
        self.mark_id = org_temp.mark_num
        #self.mark_path = f"'{org_temp.mark_dir}''{self.edit_mark_id}'.png"

    def __repr__(self):
        return f"Edit(id='{self.id}',img_file='{self.photo}',user_id='{self.user_id}',org_id='{self.org_id}',mark_id='{self.mark_id}',date_edited='{self.date_edited}')"

# editting original image and save into marked image DB folder
# class of original image DB that has columns of image id, image path,
# marked image DB folder path, marked image path(path of collectioned marked image)
# neccessary input : id, path, image_id, seg_num, part_num
# metadata : mark_num, collection_num, photo
class Original(db.Model):
    id = db.Column('org_id', db.Integer, primary_key=True)
    path = db.Column(db.String(500), unique=True, nullable=False)
    image_code = db.Column(db.String(100), nullable=False)
    seg_num = db.Column(db.Integer, nullable=False)     # corresponding segment of this component from 1~5
    part_num = db.Column(db.Integer, nullable=False)    # corresponding part of this component from 1~5

    #mark_dir = db.Column(db.String(100), unique=True, nullable=False, default=f"'{id}'default/")
    #collection_dir = db.Column(db.String(100), unique=True, nullable=False, default=f"'{id}'default/")
    photo = db.Column(LONGBLOB)   # in MySQL, it is BLOB type ---> if we save image itself to db??

    mark_num = db.Column(db.Integer, nullable=False, default=0)     # number of edits on this original image
    collection_num = db.Column(db.Integer, nullable=False, default=1)   # collected number of patterns on this original image

    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    history = db.relationship('Edit',backref='img', lazy=False)
    collected = db.relationship('Collection',backref='original', lazy=True)

    def __init__(self,path,image_code,seg_num,part_num):
        self.path = path
        self.image_code = image_code
        self.seg_num = seg_num
        self.part_num = part_num

    # collection top-k number of marked image
    # (1) collect top-k number of marked image (2) update less-efficient makred image with others
    def collectionion(self):
        return

    # updating binary image of correct path to DB
    def set_photo(self):
        with open(self.path, 'rb') as f:
            photo = f.read()
        self.photo = photo
        return photo

    # save original image to new_path
    def get_photo(self):
        data=self.photo
        return data

    # show list of editro of this original image
    def get_editor_list(self):
        history = self.history
        res = []
        for hist in history:
            res.append(hist.editor)
        return res

    def __repr__(self):
        return f"Original(id='{self.id}',path='{self.path}',iamge_id='{self.image_code}',seg_num='{self.seg_num}',part_num='{self.part_num}', mark_num='{self.mark_num}',collection_num='{self.collection_num}')"

# among marked image, collect best matching one OR top-k image in collected directory
# therefore, neccessary input will be marked_id
# neccessary input : id, org_id, edit_id, top_k
class Collection(db.Model):
    id = db.Column('col_id', db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('original.org_id'),nullable=False)
    collection_id = db.Column(db.Integer, nullable=False, default=1) # top 1
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    path = db.Column(db.String(500), unique=True, nullable=False, default= f"'{id}'.jpg")

    def __init__(self,org_id,path):
        self.org_id = org_id
        self.path = path

    def get_original(self):
        return Original.qeury.get(self.org_id)

    def get_editor(self):
        edit=self.edit[0]
        editor = edit.editor
        return editor[0]

    def __repr__(self):
        return f"collection(id='{self.id}',path='{self.path}',org_id='{self.org_id}',collection_id='{self.collection_id}')"
