from Dumble import db 



class UserInfo(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password=db.Column(db.String(length=60),nullable=False)