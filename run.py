# We import package Dumble from our folder also import app which is intialize in __init__
# and our code is run here

from Dumble import app,db


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
