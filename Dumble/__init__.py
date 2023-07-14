from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'

db=SQLAlchemy(app)
app.app_context().push()


app.config['SECRET_KEY']='95e6991c00be2df05c6671fd'
#secret key is required for post method beacuse we are submiting form 

from Dumble import routes