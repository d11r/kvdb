import sys
import os
import time
import hashlib

# --- MASTER SERVER ---

if os.environ['TYPE'] == 'master':
    import plyvel 
    db = plyvel.DB(os.environ['DB'], create_if_missing=True)

def master(env, start_response):
    key = env['REQUEST_URI'].encode('utf-8')
    metakey = db.get(key)

    # key not found
    if metakey is None:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [b"Key not found!"]
    
    # key is found (volume)
    meta = json.loads(metakey)

    # redirect
    headers = [('location', 'https://%s%s' % (meta['volume'], key))] 
    start_response('302 Found', headers)
    db.put(b'key-%d' % time.time(), b'bob')
 
# --- VOLUME SERVER ---

if os.environ['TYPE'] == 'volume':
    import socket
    host = socket.gethostname()

def volume(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hi, World!"]
