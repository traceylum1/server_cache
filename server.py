from flask import Flask
from moment import moment
from markupsafe import escape
from .cache import LRUCache
from .api import upsert, fetch

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
    upsert(key, value)
    return f'finished setting pair {escape(key)} : {escape(value)}'

@app.route('/get/<key>')
def get_result(key):
    data = lruCache.get(key)

    if data == -1 or data.staleTime >= moment.unix():
        dbVal = fetch(key)
        lruCache.set(key, dbVal)
        data = dbVal        

    return f'result for {escape(key)} - {escape(data)}'

