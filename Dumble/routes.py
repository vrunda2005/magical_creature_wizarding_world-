from Dumble import app
from Dumble import db 
from flask import render_template,redirect,url_for
from Dumble.model import UserInfo
from Dumble.forms import RegisterForm



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/creatures")
def creatures_page():
    return render_template("creatures.html")


@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register", methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=UserInfo(username=form.username.data,
                                email_address=form.email.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('creatures_page'))

    return render_template('register.html',forms=form)