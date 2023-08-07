from Dumble import app
from Dumble import db,beings_table,engine,beast_table, spirit_table,dark_table,domesticate_table, fantastic_table, plant_table, water_table
import sqlite3
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request,jsonify,g,session
from Dumble.model import UserInfo
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
def index():
    return render_template('index.html')

@app.route('/layout')
def layout_page():
    # username=current_user.id
    result=show_users()
    return render_template('layout.html',result=result)


def get_connection():
    return sqlite3.connect('instance/data.db')

#creature page 
@app.route("/creatures/<string:name>")
def creatures_page(name):
    conn = sqlite3.connect('instance/data.db')
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM {name} 
    ''')
    item = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    # info=downloading_data(name)
    limited_data = item[:4]
    conn.close()
    return render_template('creatures.html', items=item,name=name,column_names=column_names,limited_data=limited_data)


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
    conn = sqlite3.connect('instance/data.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM beast 
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM beings 
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM spirit 
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM water 
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM dark 
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM plant 
    UNION
    SELECT name,description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM domesticate 
    UNION
    SELECT name,NULL as description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM fantastic 
    ''')
    item = cursor.fetchall()    
    conn.close()
    
    return render_template("encyclopedia.html",encyclopedia=item)

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
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    form=LoginForm()
    if form.validate_on_submit():  #work when click submit  or form is validate
        #checking var with username 
        attempted_user=UserInfo.query.filter_by(username=form.username.data).first()
        #if none 
        if attempted_user and attempted_user.check_password_correction(
            attemted_password=form.password.data):
                login_user(attempted_user)
                flash(f'Success! you are logged in {current_user.username}',category='success')    
        else:
            flash('username and password not match try another ',category='danger')
    return render_template('login.html',forms=form)

# when we logged in it shows this  
@app.route("/MyAcc")  
@login_required
def logged_in():
    return render_template("MyAcc.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('you have log out ',category='info')
    return redirect(url_for('index'))


# Search function Connect to your existing database  


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



def perform_search(query):
    with engine.connect() as conn:
                beast=conn.execute(
                    beast_table.select().where(beast_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                being = conn.execute(
                    beings_table.select().where(beings_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                spirit = conn.execute(
                    spirit_table.select().where(spirit_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                water = conn.execute(
                    water_table.select().where(water_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                plant = conn.execute(
                    plant_table.select().where(plant_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                dark = conn.execute(
                    dark_table.select().where(dark_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                domesticate = conn.execute(
                    domesticate_table.select().where(domesticate_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                fantasticate= conn.execute(
                    fantastic_table.select().where(fantastic_table.c.name.ilike(f'%{query}%'))
                ).fetchall()

                result=beast+being+spirit+dark+fantasticate+domesticate+water+plant
    return result


def show_users():
    with engine.connect() as conn:
        beast = conn.execute(beast_table.select()).fetchall()
        being = conn.execute(beings_table.select()).fetchall()
        spirit = conn.execute(spirit_table.select()).fetchall()
        dark = conn.execute(dark_table.select()).fetchall()
        plant = conn.execute(plant_table.select()).fetchall()
        domesticate = conn.execute(domesticate_table.select()).fetchall()
        fantasticate = conn.execute(fantastic_table.select()).fetchall()
        water = conn.execute(water_table.select()).fetchall()
        
        result=beast+being+spirit+dark+plant+domesticate+fantasticate+water
    return result





@app.route('/<string:item_id>')
def watch_more(item_id):
    conn = sqlite3.connect('instance/data.db')
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
    SELECT name,NULL as description,habitat,behavior,abilities,reproduction,magical_significance,history,interaction_with_human_wizards,img FROM fantastic WHERE name=?
    ''', (item_id,item_id,item_id,item_id,item_id,item_id,item_id,item_id))
    item = cursor.fetchall()    
    conn.close()
    return render_template('watchmore.html', item=item)

#here starts bookmark table which is in data.db 
def create_tables():
    with sqlite3.connect('instance/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE if NOT exists bookmark(
                user_id TEXT,
                creature_id TEXT,
                FOREIGN KEY (user_id) REFERENCES user_info (username),
                FOREIGN KEY (creature_id) REFERENCES beast (id),
                UNIQUE (user_id, creature_id)
            )
        ''')
        conn.commit()

create_tables()


#this function check if user is  authenticated or not
def is_user_logged_in():
    return current_user.is_authenticated

@app.route('/bookmarks/add<string:name>')
def add_bookmark(name):
    if is_user_logged_in():
        user_id = current_user.username
        with sqlite3.connect('instance/data.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO bookmark (user_id, creature_id) VALUES (?, ?)', (user_id, name))
                conn.commit()
                flash('message: Bookmark added successfully!',category='success')
                # return "message: Bookmark added successfully!"
            except sqlite3.IntegrityError:
                flash('message: B"Bookmark already exists!',category='success')       
    else:
        flash('message: "Please log in to add bookmarks',category='danger')
    return redirect(url_for('creatures_page',name='beast'))
        
    
@app.route('/showbookmark/')
@login_required
def showbookmark():
    user_id = current_user.username

    with sqlite3.connect('instance/data.db') as conn:
        cursor = conn.cursor()
    #     query=f'''SELECT {table}.*,
    #                bookmark.user_id
    #         FROM {table}
    #         JOIN bookmark ON {table}.name = bookmark.creature_id
    #         WHERE bookmark.user_id = ?
            

    #         '''
        
        cursor.execute('''
            SELECT beast.*,
                   bookmark.user_id
            FROM beast
            JOIN bookmark ON beast.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
            UNION
            SELECT beings.*,
                   bookmark.user_id
            FROM beings
            JOIN bookmark ON beings.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
            UNION
            SELECT spirit.*,
                   bookmark.user_id
            FROM spirit
            JOIN bookmark ON spirit.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
            
            UNION
            SELECT dark.*,
                   bookmark.user_id
            FROM dark
            JOIN bookmark ON dark.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
                       
            UNION
            SELECT plant.*,
                   bookmark.user_id
            FROM plant
            JOIN bookmark ON plant.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
                       
            UNION
            SELECT water.*,
                   bookmark.user_id
            FROM water
            JOIN bookmark ON water.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
                       
            UNION
            SELECT domesticate.*,
                   bookmark.user_id
            FROM domesticate
            JOIN bookmark ON domesticate.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
                       
            UNION
            SELECT fantastic.*,
                   bookmark.user_id
            FROM fantastic
            JOIN bookmark ON fantastic.name = bookmark.creature_id
            WHERE bookmark.user_id = ?
                       
        ''', (user_id,user_id,user_id,user_id,user_id,user_id,user_id,user_id))

        # cursor.execute(query,(user_id,))
        bookmarked_beasts = cursor.fetchall()
        # conn.commit()
        # conn.close()
    return render_template('books.html', bookmarked_beasts=bookmarked_beasts,user_id=user_id)

@app.route('/delete_bookmark/<string:bookmark_id>')
def delete_bookmark(bookmark_id):

    try:
        conn = sqlite3.connect('instance/data.db')
        cursor = conn.cursor()

        # Check if the bookmark ID exists in the Bookmark table
        cursor.execute("SELECT COUNT(*) FROM bookmark WHERE bookmark.creature_id = ?", (bookmark_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            # Delete the bookmark with the specific ID if it exists
            cursor.execute("DELETE FROM bookmark WHERE bookmark.creature_id = ?", (bookmark_id,))
            conn.commit()
            conn.close()
            flash("message Bookmark deleted successfully.",category='success')
        else:
            conn.close()
            flash("you have not added to fav",category='danger')
        # db.session.delete(bookmark_id)
        # db.session.commit()
        # flash(f"Bookmark with ID {bookmark_id} deleted successfully.", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error occurred while deleting bookmark: {str(e)}", 'danger')

    return render_template('creatures.html')  
