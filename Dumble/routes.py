from Dumble import app
from Dumble import db 
import sqlite3
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request
from Dumble.model import UserInfo
from Dumble.forms import RegisterForm,LoginForm
from flask_login import login_user
from Dumble.forms import RegisterForm,LoginForm
from flask_bcrypt import Bcrypt
from Dumble import bcrypt
from flask_login import login_manager,logout_user,login_required, login_user,LoginManager,current_user

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login_page"

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


   
#this is condition for user to login to watch all website
@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username)


@app.route("/creatures")
def creatures_page():
    return render_template("creatures.html")

@app.route("/beast")
def beast_page():
    return render_template("beast.html")

@app.route("/encyclopedia")
def encyclopedia():
    return render_template("encyclopedia.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


#Register code starts 
@app.route("/register", methods=['GET','POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
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

#login code starts 
@app.route("/login",methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():  #work when click submit  or form is validate
        #checking var with username 
        attempted_user=UserInfo.query.filter_by(username=form.username.data).first()
        #if none 
     
        if attempted_user and attempted_user.check_password_correction(
            attemted_password=form.password.data):

                login_user(attempted_user)
                flash('Success! you are logged in {{attempted_user.name}}',category='success')
                return redirect(url_for('creatures_page'))

        else:
            flash('username and password not match try another ',category='danger')
    return render_template('login.html',forms=form)

# when we logged in it shows this  
@app.route("/MyAcc")  
def logged_in():
    return render_template("MyAcc.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('you have log out ',category='info')
    return redirect(url_for('index'))


# Search function Connect to your existing database  
def get_connection():
    return sqlite3.connect('instance/demo.db')

@app.route('/')
def Todo_list():
    return render_template('search.html', results=get_all_items())

@app.route('/search', methods=['GET','POST'])
def search():
    query = request.args.get('query')
    if not query:
        # If no search query is provided, show all data
        results = get_all_items()
        return render_template('search.html',results=results)
    else:
        # Filter data based on search query
        results = search_items(query)

    return render_template('beast.html', results=results)

def get_all_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT Name FROM magic')
    
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

def search_items(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM magic WHERE Name LIKE ?', ('%' + query + '%',))
    data=cursor.fetchall()
    items = [row[0] and row[1] and row[3] for row in cursor.fetchall()]
    conn.close()
    return data






























































































# @app.route("/login",methods=['GET','POST'])
# def login_page():
#     if current_user.is_authenticated:
#         return redirect(url_for('MyAcc'))
#     form=LoginForm()
#     if form.validate_on_submit():
#         user=UserInfo.query.filter_by(username=form.username.data).first()
#         if user:
#             if user and bcrypt.check_password_hash(user.password,form.password.data) is not False:
#                    login_user(user)  
#                    return redirect(url_for('MyAcc'))  
#             else:
#                 flash('Login Unsuccessful Make sure you have created account','danger')    