from Project import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(admin_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key = True)
    # profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    name=db.Column(db.String(128))
    email = db.Column(db.String(64),unique = True,index=True)
    dob=db.Column(db.DateTime())
    gender=db.Column(db.String(64))
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    # spot_visited = db.relationship('Tourist_Spot_Visited',backref='spot_visited',lazy=True)

    def __init__(self,name,email,dob,gender,username,password):
        self.name = name
        self.email = email
        self.dob =dob
        self.gender = gender
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"username {self.username}"

class Admin(db.Model,UserMixin):
    __tablename__ = 'admins'
    id=db.Column(db.Integer,primary_key = True)
    name=db.Column(db.String(128))
    email = db.Column(db.String(64),unique = True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self,name,email,username,password):
        self.name =name
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

#db.create_all()
# class Tourist_Spot(db.Model):
#     pass
#
# class User_Visited(db.Model):
#     users = db.relatiosnhip(User)
#
#     id = db.Column(db.Integer,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
#     # Also enter relationship field for Tourist Spot
#     rating = db.Column(db.Integer,nullable=False)
#     text = db.Column(db.Text,nullable=False)
#
#     def __init__(self,user_id,spot_id,text):
#         self.user_id = user_id;
#         self.spot_id = spot_id;
#         self.text = text;
#
#     def __repr__(self):
#         return f"Tourist Spot Visited: {self.id},{self.spot_id} by {self.user_id}"
#
# class User_Recommendations(db.Model):
#     pass
