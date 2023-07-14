from Dumble import db 
from Dumble import bcrypt


class UserInfo(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password=db.Column(db.String(length=60),nullable=False)

    # def __repr__(self):
    #     return f'User '

    @property
    def password(self):
            return self.password

    @password.setter
    def password(self,plain_text_password):
            self.password=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

