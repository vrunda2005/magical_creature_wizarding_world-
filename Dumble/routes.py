from Dumble import app
from Dumble import db 
from flask import render_template,redirect,url_for,flash,get_flashed_messages
from Dumble.model import UserInfo
from Dumble.forms import RegisterForm,LoginForm
from flask_login import login_user


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/creatures")
def creatures_page():
    return render_template("creatures.html")


@app.route("/register", methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=UserInfo(username=form.username.data,
                                email_address=form.email.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('creatures_page')) #for checking its working or not we have to change it further
    if form.errors !={}: #if there are not errors form validations 
        for err_msg in form.errors.values():
            flash(f'ERROR{err_msg}',category='danger')
            
    return render_template('register.html',forms=form)

@app.route("/login",methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():  #work when click submit  or form is validate
        #checking var with username 
        attempted_user=UserInfo.query.get(form.username.data).first()
        #if none 
        if attempted_user and attempted_user.check_password_correction(
            attemted_password=form.password.data):

                login_user(attempted_user)
                flash('Success! you are logged in {{attempted_user.name}}',category='success')
                return redirect(url_for('creatures_page'))

        else:
            flash('username and password not match try another ',category='danger')
    return render_template('login.html',forms=form)