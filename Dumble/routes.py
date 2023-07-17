from Dumble import app
from Dumble import db 
from flask import render_template,redirect,url_for,flash,get_flashed_messages
from Dumble.model import UserInfo
from Dumble.forms import RegisterForm
from flask_bcrypt import Bcrypt
from Dumble import bcrypt
from flask_login import login_manager,logout_user,login_required, login_user,log

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/creatures")
def creatures_page():
    return render_template("creatures.html")

@app.route("/beast")
def beast_page():
    return render_template("beast.html")


@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register", methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
      
        hash_password=bcrypt.generate_password_hash(form.password1.data) #entered password converts into hash password
        user_to_create=UserInfo(username=form.username.data,
                                email_address=form.email.data,
                                password=hash_password)
        #storing data to our database 
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page')) #for checking its working or not we have to change it further
    if form.errors !={}: #if there are not errors form validations 
        for err_msg in form.errors.values():
            flash(f'ERROR{err_msg}',category='danger')
            

    return render_template('register.html',forms=form)