from flask import Flask, redirect, render_template, request, url_for
from firebase_admin import credentials, firestore, initialize_app, _apps

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
if not _apps:
    cred = credentials.Certificate("./newkey.json") 
    firebase = initialize_app(cred)

db = firestore.client()
notes_ref = db.collection('notes')

@app.route('/', methods=['GET'])
def home():
    docs = notes_ref.get()
    notes = [doc.to_dict() for doc in docs]
    
    return render_template("index.html", notes = notes)

@app.route('/add', methods=['POST'])
def add():
    """
        add() : Add a document from Firestore collection 
    """
    note = {
        'text': request.form['text']
    }
    app.logger.info(request.form['text'])
    notes_ref.add(note)
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update():
    """
        update() : Update a document from Firestore collection 
    """
    app.logger.info(request.form)

    value = request.form["text"] 
    data={
        "text": f"{value} but updated"
    }    
    doc = notes_ref.where("text", "==", value).get()[0]
    notes_ref.document(doc.id).update(data)
    return redirect(url_for('home'))
    

@app.route('/delete', methods=['POST'])
def delete(): 
    """
        delete() : Delete a document from Firestore collection 
    """
    value = request.form["text"]
    doc = notes_ref.where("text", "==", value).get()[0] 
    notes_ref.document(doc.id).delete()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)