from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


class User(UserMixin,db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer,primary_key = True)
   username = db.Column(db.String(255))
   email=db.Column(db.String(255),unique=True,index=True)
   password_hash=db.Column(db.String(255))
   pass_secure = db.Column(db.String(255))
   about = db.Column(db.String(255))
   profile_pic_path = db.Column(db.String())
   pitch = db.relationship('Pitch', backref='user', lazy='dynamic')
   pitchcom = db.relationship('PitchCom', backref='user', lazy='dynamic')


   @property
   def password(self):
       raise AttributeError('You can`t see this')
   @password.setter
   def password(self, password):
       self.pass_secure = generate_password_hash(password)
   def verify_password(self,password):
       return check_password_hash(self.pass_secure,password)
   def __repr__(self):
       return  {self.username}
   @login_manager.user_loader
   def load_user(user_id):
       return User.query.get(int(user_id))


class Pitch(db.Model):
   __tablename__ = 'pitch'
   id = db.Column(db.Integer, primary_key=True)
   pitch = db.Column(db.String(255))
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   pitchdata = db.relationship('PitchCom', backref='use', lazy='dynamic')
   def save_pitch(self):
       db.session.add(self)

       
class PitchCom(db.Model):
   __tablename__ = 'pitchcom'
   id = db.Column(db.Integer, primary_key=True)
   Pitchcom = db.Column(db.String(255))
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   pitch_id = db.Column(db.Integer, db.ForeignKey("pitch.id"))
   def save_pitchcom(self):
       db.session.add(self)
       db.session.commit()
