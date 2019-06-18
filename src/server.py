import json
import os
import time
import hashlib

from src.constants import *
from src.file_cache import FileCache

# --- MASTER SERVER ---

if os.environ['TYPE'] == 'master':
    volumes = os.environ['VOLUMES'].split(',')

    for v in volumes:
        print(v)

    import plyvel
    db = plyvel.DB(os.environ['DB'], create_if_missing=True)


def master(env, start_response):
    key = env['REQUEST_URI'].encode('utf-8')
    metakey = db.get(key)

    if metakey is None:
        if env['REQUEST_METHOD'] == 'POST':
            # handler for data insertion
            # TODO: figure out which Volume server to connect to
            pass

        start_response(NOT_FOUND, TEXT_PLAIN)
        return KEY_NOT_FOUND

    # key is found
    meta = json.loads(metakey)

    # redirect for either [GET, DELETE]
    headers = [('location', 'https://%s%s' % (meta['volume'], key))]
    start_response(FOUND, headers)
    db.post(b'key-%d' % time.time(), b'bob')


# --- VOLUME SERVER ---

if os.environ['TYPE'] == 'volume':
    import socket

    host = socket.gethostname()

    # create file cache
    fc = FileCache(os.environ['VOLUME'])


def volume(env, start_response):
    key = env['REQUEST_URI'].encode('utf-8')
    hashkey = hashlib.md5(key).hexdigest()

    if env['REQUEST_METHOD'] == 'GET':
        if not fc.exists(hashkey):
            # key not in cache
            start_response(NOT_FOUND, TEXT_PLAIN)
            return KEY_NOT_FOUND
        return [fc.get(hashkey)]

    if env['REQUEST_METHOD'] == 'POST':
        file_len = int(env.get('CONTENT_LENGTH', '0'))
        fc.post(hashkey, env['wsgi.input'].read(file_len))

    if env['REQUEST_METHOD'] == 'DELETE':
        fc.delete(hashkey)
