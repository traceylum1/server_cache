from flask import Flask
from markupsafe import escape
from .cache import LRUCache
from .api import db_upsert, db_fetch

options = {
    'capacity': 2,     # default 100
    'staleTime': 5*60   # 5 mins (default immediate)
}

lruCache = LRUCache(options)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, world!</p>'

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content

@app.route('/set/<key>/<value>')
def set_data(key, value):
    lruCache.set(key, value)
    db_upsert(key, value)
    return f'Finished setting pair {escape(key)} : {escape(value)}'

@app.route('/get/<key>')
def get_result(key):
    data = lruCache.get(key)

    if data == None:
        dbVal = db_fetch(key)
        if dbVal == None:
            return f'No records found for {escape(key)}'
        lruCache.set(key, dbVal)
        data = dbVal

    return f'Result for {escape(key)} - {escape(data)}'

