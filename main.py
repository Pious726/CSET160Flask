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
        return render_template('boat_create.html', error = None, success = "Successful")
    except:
        return render_template('boat_create.html', error = "Failed", success = None)

@app.route('/boatDelete', methods=["GET"])
def getBoatForDelete():
    return render_template('boat_delete.html')

@app.route('/boatDelete', methods=["POST"])
def deleteBoat():
    try:
        conn.execute(text('delete from boats where id = '))
        return render_template('boat_delete.html', error = None, success = "Successful")
    except:
        return render_template('boat_delete.html', error = "Failed", success = None)



if __name__ == '__main__':
    app.run(debug=True)