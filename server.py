import os
from flask import Flask, redirect, render_template, request, jsonify, url_for
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB


cred = credentials.Certificate("./newkey.json")
firebase= initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')


@app.route('/', methods=['GET'])
def home():
    docs = db.collection('notes').get()
    print(docs)    
    notes = [doc.to_dict() for doc in docs]
    
    print(notes)
    return render_template("index.html", notes = notes)

@app.route('/add', methods=['POST'])
def create():
    note = {
        'text': request.form['text']
    }
    db.collection('notes').add(note)
    return redirect(url_for('home'))

@app.route('/update', methods=['PUT'])
def update(text):
    data={
        "text": text
    }
    db.collection('notes').update(data)

@app.route('/delete', methods=['DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0')