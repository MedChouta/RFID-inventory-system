from flask import Flask, render_template, request, g, redirect
from datetime import datetime
import sqlite3

#=====Global========
addingMode = False
tagUID = ""
items_picked = set()
#===================

app = Flask(__name__)


notLoggedIn = True
DATABASE = 'Database.db'


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)

    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()

    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/picked")
def confirmPickUp():
    global items_picked
    if request.args.get("status") is not None:
        if request.args.get("status") == "yes":
            for el in items_picked:
                print("ELEMENT: " + el)
                unclassify(el)
                print("UNCLASSIFIED")
            items_picked = set()
    return {"items_picked": len(items_picked)}, 302

@app.route("/picked/<id>")
def itemsPicked(id):
    print(f"itemsPickd: {id}")
    global items_picked
    items_picked.add(id)
    return {"items_picked": len(items_picked)}, 302


@app.route("/", methods=['GET', 'POST'])
def index():
    total = []
    items = set()
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        if email is not None and password is not None:

            if request.form['email'] and request.form["password"]:
                for user in query_db('select * from users'):
                    if email == user['email'] and password == user['password']:
                        global notLoggedIn
                        notLoggedIn = False
    
    return render_template("index.html", login=notLoggedIn, items=getItems())

@app.route("/notifications")
def notification():
    if request.method == 'GET':
        if request.args.get("message") is not None:
            content = request.args.get("message")
            query_db('INSERT INTO notifications (content, date) VALUES (?, ?)', (content, datetime.now()))
        
        notifications = query_db('SELECT * FROM notifications')

        return render_template("notifications.html", login=notLoggedIn, items=getItems())
    
    return {"error": "Forbidden"}, 404


def itemExist(id):
    items = getItems()

    for item in items:
        if id == item["item_id"]:
            return True
    
    return False


@app.route("/addtag", methods=["GET", "POST"])
def addTag():
    if request.method == 'GET':
        if request.args.get("tag_id") is not None:
            global tagUID
            tagUID = request.args.get("tag_id")
            print("TAG UID TYPE: " + str(type(tagUID)))
            return {"id": tagUID}, 302
        print("no tagID")
    return {"error": "Forbidden"}, 403
    

@app.route("/add", methods= ["GET", "POST"])
def addItem():
    if request.method == 'POST':
        name = request.form["name"]
        location = request.form["location"]

        global addingMode
        addingMode = True


        global tagUID
        while tagUID == "":
            pass
        

        if (name is not None) and (location is not None) and not itemExist(tagUID):
            if isUnclassified(tagUID):
                classify(tagUID)
                
            print(name)
            print(location)
            print(tagUID)
            query_db('INSERT INTO items (name, item_id, location, date) VALUES (?, ?, ?, ?)', (name, tagUID, location, datetime.now()))

        tagUID = ""
        addingMode = False
        return redirect("/", code=302)
        
    else:
        return render_template("add.html", type=False)

@app.route("/adduser", methods=["GET", "POST"])
def addUser():
    if request.method == 'POST':
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            email = request.form["email"]
            password = request.form["password"]
            

            if (firstname is not None) and (lastname is not None) and (email is not None) and (password is not None) and not userExists(email):
                query_db('INSERT INTO users (firstname, lastname, email, password, date) VALUES (?, ?, ?, ?, ?)', (firstname, lastname, email, password, datetime.now()))
                global notLoggedIn
                notLoggedIn = False
                return redirect("/", code=302)
    else:
        return {"error": "No args"}, 400

def userExists(email):
    for user in getUsers():
        if email == user["email"]:
            return True
    
    return False

@app.route("/mode")
def mode():
    global addingMode
    if addingMode:

        return "", 200
    
    return {"error": "Forbidden"}, 403

def getItems():
    return query_db('SELECT * FROM items')

@app.route("/getItem/<id>")
def getItemsWithId(id):
    print(id)
    item = query_db(f"SELECT * FROM items WHERE item_id=?", (str(id),)) 
    if len(item) > 0:
        return item[0], 302
    
    return {}, 302

def getUsers():
    return query_db('SELECT * FROM users')

@app.route("/del/<id>")
def deleteItems(id):

    if id is not None:
        query_db('DELETE FROM items where id=?', (str(id),))
        return redirect("/", code=302)
    else:
        return {"error": "No id"}, 400


def isUnclassified(id):
    getItem = query_db('SELECT * FROM unclassified WHERE item_id=?', (str(id),))

    if len(getItem) > 0:
        return True
    else:
        return False
    
def classify(id):
    query_db('DELETE FROM unclassified where item_id=?', (str(id),))

def unclassify(id):
    (item,code) = getItemsWithId(id)
    query_db('DELETE FROM items where item_id=?', (str(id),))

    getItem = query_db('SELECT * FROM unclassified WHERE item_id=?', (str(id),))
    if len(getItem) == 0:
        query_db('INSERT INTO unclassified (name, item_id, date) VALUES (?, ?, ?)', (item["name"], item["item_id"], datetime.now()))   
    else:     
        for it in getItem:
            if it["item_id"] == id:
                query_db('INSERT INTO unclassified (name, item_id, date) VALUES (?, ?, ?)', (item["name"], item["item_id"], datetime.now()))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)