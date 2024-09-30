# save this as webserver.py
from flask import Flask, request
from resources import EntryManager, Entry

app = Flask(__name__)
FOLDER = './files/'

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/api/entries/")
def get_entries():
    e_man = EntryManager(FOLDER)
    e_man.load()
    list_of_dict_entries = [entry.json() for entry in e_man.entries]
    return list_of_dict_entries

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    e_manager = EntryManager(FOLDER)
    content = request.get_json()
    for e in content:
        entry = Entry.from_json(e)
        e_manager.entries.append(entry)
    e_manager.save()
    return {"status": "success"}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)


