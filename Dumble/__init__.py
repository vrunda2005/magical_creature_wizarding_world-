# __init__ file is main file for Dumble folder
# Module Initialization: The __init__.py file can also contain Python code that
# will be executed when the package is imported in run.py (outside Dumble). This initialization code can define variables,
# import submodules, or perform any other necessary setup.
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os 
def configure():
        load_dotenv()

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

app.app_context().push()

with app.app_context():
        db.create_all() 
        
def convert(val):
        if type(val) != str:
                return val
        if val.isnumeric():
                return int(val)
        elif val == 'True':
                return True
        elif val == 'False':
                return False
        else:
                return val
app.config['SECRET_KEY']='95e6991c00be2df05c6671fd'

#secret key is required for post method beacuse we are submiting form 


#hash password not number 
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)


engine = create_engine('sqlite:///instance/data.db')
metadata = MetaData()
metadata.reflect(bind=engine)

beings_table = Table('beings', metadata, autoload=True, autoload_with=engine)
beast_table = Table('beast', metadata, autoload=True, autoload_with=engine)
spirit_table    =Table('spirit', metadata, autoload=True, autoload_with=engine)
dark_table       =Table('dark', metadata, autoload=True, autoload_with=engine)
domesticate_table=Table('domesticate', metadata, autoload=True, autoload_with=engine)
fantastic_table  =Table('fantastic', metadata, autoload=True, autoload_with=engine)
plant_table      =Table('plant', metadata, autoload=True, autoload_with=engine)
water_table      =Table('water', metadata, autoload=True, autoload_with=engine)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# app.config['SQLALCHEMY_BINDS'] = {
#     'second_db': 'sqlite:///beast.db'
# }


from Dumble import routes

