from Dumble import db 
from flask_login import UserMixin
from Dumble import bcrypt


# For storing data of user in our database and convert it into hash password 

class UserInfo(db.Model,UserMixin): #creted table for database 
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password=db.Column(db.String(length=60),nullable=False)

    # def __repr__(self):
    #     return f'User '

    def check_password_correction(self,attemted_password):
           return bcrypt.check_password_hash(self.password,attemted_password)
                  
