from Dumble import app
from Dumble import db,beings_table,engine,beast_table
import sqlite3
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request,jsonify,g,session
from Dumble.model import UserInfo,Bookmark
from Dumble.forms import RegisterForm,LoginForm
from flask_login import login_user
from Dumble.forms import RegisterForm,LoginForm
from flask_bcrypt import Bcrypt
from Dumble import bcrypt
from flask_login import login_manager,logout_user,login_required, login_user,LoginManager,current_user
from sqlalchemy import select,Column,TEXT,text

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect



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

@app.route('/layout')
def layout_page():
    result=show_users()
    return render_template('layout.html',result=result)

@app.route("/beings")
def beings_page():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM beings')
    items = [row for row in cursor.fetchall()]
    conn.close()
    return render_template("beast.html",items=items)

@app.route("/domesticate")
def domesticate_page():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM domesticate')
    items = [row for row in cursor.fetchall()]
    conn.close()
    return render_template("beast.html",items=items)

@app.route("/plant")
def plant_page():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plant')
    items = [row for row in cursor.fetchall()]
    conn.close()
    return render_template("beast.html",items=items)

@app.route("/darkcreatures")
def darkcreatures_page():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dark')
    items = [row for row in cursor.fetchall()]
    conn.close()
    return render_template("beast.html",items=items)

@app.route("/watercreatures")
def watercreatures_page():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM water')
    items = [row for row in cursor.fetchall()]
    conn.close()
    return render_template("beast.html",items=items)

@app.route("/spirit")
def spirit_page():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM spirit') 
    items = [row for row in cursor.fetchall()]
    conn.close()
    return render_template("beast.html",items=items)

def get_connection():
    return sqlite3.connect('D:\harry_hermione_ron\website\instance/beast.db')

# @app.route("/beast")
# def beast_page():
#     conn = get_connection()
#     cursor = conn.cursor()
#     rows = cursor.fetchall()
#     cursor.execute('SELECT * FROM beast')
#     items = [row for row in cursor.fetchall()]
#     column_names = [description[0] for description in cursor.description]
#     # info=downloading_data()
#     # col=[name for name in info]
#     cursor.close()
#     conn.close()
#     return render_template("beast.html",items=items)

#creature page 
@app.route("/beast/<string:name>")
def beast_page(name):
    name=name
    conn = sqlite3.connect('instance/beast.db')
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM {name} 
    ''')
    item = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    info=downloading_data(name)
    conn.close()
    return render_template('beast.html', items=item,name=name,column_names=column_names,info=info)


#to show  information or defination about creature 
def downloading_data(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT info FROM {name} LIMIT 1;')
    items = cursor.fetchone()
    conn.close()
    return items


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


# @app.route('/todo')
# def todo():
#     return render_template('layout.html',results=get_all_items())

@app.route('/search', methods=['GET','POST'])
def search():
    query = request.form.get('query')
    # query = request.args.get('query')
    if not query:
        results = show_users()
        return render_template('layout.html', results=results)
    else:
        # Filter data based on search query
        results = perform_search(query)
    return render_template('seacr_creatures.html', results=results)

#not for now implemented multiple table database connect 
# def get_all_items():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT name FROM Beast')
#     items = [row for row in cursor.fetchall()]
#     conn.close()
#     return items

#not for now implemented multiple table database connect 
# def search_items(query):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM Beast WHERE name LIKE ? ", ('%' + query + '%',))
#     data=cursor.fetchall()
#     items = [row[0] and row[1] and row[3] for row in cursor.fetchall()]
#     conn.close()
#     return data


def perform_search(query):
    with engine.connect() as conn:
                beast=conn.execute(
                    beast_table.select().where(beast_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                being = conn.execute(
                    beings_table.select().where(beings_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                result=beast+being
    return result


def show_users():
    with engine.connect() as conn:
        beast = conn.execute(beast_table.select()).fetchall()
        being = conn.execute(beings_table.select()).fetchall()
        result=beast+being
    return result





@app.route('/more/<string:item_id>')
def show_more(item_id):
    conn = sqlite3.connect('instance/beast.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM beast WHERE name=?
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM beings WHERE name=?
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM spirit WHERE name=?
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM water WHERE name=?
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM dark WHERE name=?
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM plant WHERE name=?
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM domesticate WHERE name=?
    UNION
    SELECT name,NULL as description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM fanatastic WHERE name=?
    ''', (item_id,item_id,item_id,item_id,item_id,item_id,item_id,item_id))
    
    # cursor.execute("SELECT * FROM beast_new,water,beings_new WHERE name=?", (item_id,))
    # cursor.execute("SELECT * FROM water WHERE name=?", (item_id,))
    # cursor.execute("SELECT * FROM beings_new WHERE name=?", (item_id))
    item = cursor.fetchall()
    # column_names = [description[0] for description in cursor.description]
    
    conn.close()

    return render_template('watchmore.html', item=item)

#here starts bookmark table which is in data.db 
# def create_tables():
#     with sqlite3.connect('instance/data.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE bookmarks (
#                 user_id INTEGER,
#                 creature_id INTEGER,
#                 FOREIGN KEY (user_id) REFERENCES user_info (username),
#                 FOREIGN KEY (creature_id) REFERENCES beast (id),
#                 UNIQUE (user_id, creature_id)
#             )
#         ''')
#         conn.commit()
# create_tables()


#this function check if user is  authenticated or not
def is_user_logged_in():
    return current_user.is_authenticated

@app.route('/bookmarks/add<string:name>')
def add_bookmark(name):
    if is_user_logged_in():
        user_id = current_user.id
        # item_id = request.json['item_id']
    
        with sqlite3.connect('instance/data.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO bookmarks (user_id, creature_id) VALUES (?, ?)', (user_id, name))
                conn.commit()
                flash('message: Bookmark added successfully!',category='success')
                # return "message: Bookmark added successfully!"
            except sqlite3.IntegrityError:
                flash('message: B"Bookmark already exists!',category='success')
                
    else:
        flash('message: "Please log in to add bookmarks',category='danger')
    return render_template('index.html')
        
    


#show function mai thode loche hee 
@app.route('/showbookmark')
@login_required
def showbookmark():
    user_id = current_user.id

    with sqlite3.connect('instance/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT beast.*,
                   bookmarks.user_id
            FROM beast
            JOIN bookmarks ON beast.name = bookmarks.creature_id
            WHERE bookmarks.user_id = ?
        ''', (user_id,))
        bookmarked_beasts = cursor.fetchall()

    return render_template('books.html', bookmarked_beasts=bookmarked_beasts,user_id=user_id)



