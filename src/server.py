import json
import os
import time
import hashlib

from src.file_cache import FileCache

# --- MASTER SERVER ---

if os.environ['TYPE'] == 'master':
    import plyvel

    db = plyvel.DB(os.environ['DB'], create_if_missing=True)


def master(env, start_response):
    key = env['REQUEST_URI'].encode('utf-8')
    metakey = db.get(key)

    if metakey is None:
        if env['REQUEST_METHOD'] == 'PUT':
            # handler for data insertion
            # TODO: figure out which Volume server to connect to
            pass

            # key does not exist & no interest in creating it
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [b"Key not found!"]

    # key is found
    meta = json.loads(metakey)

    # redirect for either [GET, DELETE]
    headers = [('location', 'https://%s%s' % (meta['volume'], key))]
    start_response('302 Found', headers)
    db.put(b'key-%d' % time.time(), b'bob')


# --- VOLUME SERVER ---

if os.environ['TYPE'] == 'volume':
    import socket

    host = socket.gethostname()

    # register with master
    master = os.environ['MASTER']

    # create file cache
    fc = FileCache(os.environ['VOLUME'])


def volume(env, start_response):
    key = env['REQUEST_URI'].encode('utf-8')
    hashkey = hashlib.md5(key).hexdigest()

    if not fc.exists(hashkey):
        pass
