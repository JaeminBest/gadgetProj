# models.py
# author : jaemin kim
# Last-edited : 2019-04-29 4PM
# details : back-end server DB model that describe user, original image, edits from users, and collection of edits that used for actual machine learning

# connection with database.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base

# data types
from sqlalchemy.dialects.mysql import LONGBLOB
import datetime


# schema : users(id, username, email, password, deleted)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    deleted = Column(Boolean, default=False)

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        self.deleted = False

    def __repr__(self):
        return f"User(id='{self.id}',username='{self.username}',email='{self.email}', deleted='{self.deleted}')"

    def delete_user(self):
        if not self.deleted:
            self.deleted = True
            return True
        else:
            return False


# schema : originals(id, label_num, part_num, image_code, data)
class Original(Base):
    __tablename__ = 'originals'
    id = Column(Integer, primary_key=True)
    label_num = Column(String(3), nullable=False)
    part_num = Column(Integer, nullable=False)
    image_code = Column(String(100), nullable=False)
    data = Column(LONGBLOB)

    def __init__(self, label_num, part_num, image_code):
        self.image_code = image_code
        self.label_num = label_num
        self.part_num = part_num

    def __repr__(self):
        return f"Original(id='{self.id}',image_code='{self.image_code}',label_num='{self.label_num}',part_num='{self.part_num}')"

    # updating binary image of correct path to DB
    def set_photo(self, path):
        with open(path, 'rb') as f:
            data = f.read()
        self.data = data

    # save original image to new_path
    def get_photo(self):
        data=self.data
        return data


# schema : marks(id, user_id, org_id, date_edited, data, deleted)
class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) # decide by user
    org_id = Column(Integer, ForeignKey('originals.id'), nullable=False) # decide by clicking specific original image
    data = Column(LONGBLOB)
    date_edited = Column(DateTime, nullable=True)
    deleted = Column(Boolean, default=False)

    def __init__(self, user_id, org_id, data):
        self.user_id = user_id
        self.org_id = org_id
        self.date_edited = datetime.utcnow()
        self.data = data

    def __repr__(self):
        return f"Mark(id='{self.id}',user_id='{self.user_id}',org_id='{self.org_id}',date_edited='{self.date_edited}',data='{self.data}',deleted='{self.deleted}')"
