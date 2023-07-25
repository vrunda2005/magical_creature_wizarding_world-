# __init__ file is main file for Duble folder
# Module Initialization: The __init__.py file can also contain Python code that
# will be executed when the package is imported in run.py (outside Dumble). This initialization code can define variables,
# import submodules, or perform any other necessary setup.

from flask import Flask
from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

app.app_context().push()


app.config['SECRET_KEY']='95e6991c00be2df05c6671fd'
#secret key is required for post method beacuse we are submiting form 


#hash password not number 
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)


engine = create_engine('sqlite:///D:\harry_hermione_ron\website\instance/beast.db')
metadata = MetaData()
metadata.reflect(bind=engine)
beings_table = Table('beings', metadata, autoload=True, autoload_with=engine)
beast_table = Table('Beast', metadata, autoload=True, autoload_with=engine)




from Dumble import routes
