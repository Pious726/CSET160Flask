from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/boats')
def boats():
    boats = conn.execute(text('select * from boats')).all()
    return render_template('boats.html', boats = boats[:10])

@app.route('/boatCreate', methods=["GET"])
def getBoat():
    return render_template('boat_create.html')

@app.route('/boatCreate', methods=["POST"])
def createBoat():
    try:
        conn.execute(text('insert into boats values(:id, :name, :type, :owner_id, :rental_price)'), request.form)
        conn.commit()
        return render_template('boat_create.html', error = None, success = "Successful")
    except:
        return render_template('boat_create.html', error = "Failed", success = None)

@app.route('/boatDelete', methods=["GET"])
def getBoatForDelete():
    boats = conn.execute(text('select * from boats')).fetchall()
    return render_template('boat_delete.html', boats=boats)

@app.route('/boatDelete', methods=["POST"])
def deleteBoat():
    try:
        conn.execute(text('delete from boats where id = :id'), request.form)
        conn.commit()
        return render_template('boat_delete.html', error = None, success = "Successful")
    except:
        return render_template('boat_delete.html', error = "Failed", success = None)

@app.route('/boatSearch', methods=["GET"])
def getBoatForSearch():
    boats = conn.execute(text('select id from boats')).fetchall()
    return render_template('boat_search.html', boats=boats)

@app.route('/boatSearch', methods=["POST"])
def searchBoat():
    try:
        search = conn.execute(text('select * from boats where id = :id'), request.form).fetchone()
        return render_template('boat_search.html', boat = search, error = None, success = "Successful")
    except:
        return render_template('boat_search.html', boat = None, error = "Failed", success = None)

@app.route('/boatUpdate', methods=["GET"])
def getBoatForUpdate():
    boats = conn.execute(text('select * from boats')).fetchall()
    return render_template('boat_update.html', boats=boats)

@app.route('/boatUpdate', methods=["POST"])
def updateBoat():
    try:
        conn.execute(text('update boats set name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price where id = :id'), request.form)
        conn.commit()
        return render_template('boat_update.html', error = None, success = "Successful")
    except:
        return render_template('boat_update.html', error = "Failed", success = None)
    

if __name__ == '__main__':
    app.run(debug=True)