from Dumble import db 
from flask_login import UserMixin


class UserInfo(db.Model,UserMixin): #creted table for database 
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password=db.Column(db.String(length=60),nullable=False)

    # def __repr__(self):
    #     return f'User '
#g=for hash password 
    @property
    def password(self):
            return self.password

    @password.setter
    def password(self, plain_text_password):
            self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attemted_password):
           return bcrypt.check_password_hash(self.password_hash,attemted_password)
                  
