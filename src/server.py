import json
import os
import random
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
    key = env['REQUEST_URI']
    metakey = db.get(key.encode('utf-8'))

    if metakey is None:
        if env['REQUEST_METHOD'] == 'POST':
            # handler for data insertion
            # TODO: volume selection should not be random
            volume = random.choice(volumes)

            # store metakey in db
            metakey = json.dumps({"volume": volume})
            db.put(key.encode('utf-8'), metakey.encode('utf-8'))
        else:
            start_response(NOT_FOUND, TEXT_PLAIN)
            return KEY_NOT_FOUND
    else:
        # key is found
        """
        if env['REQUEST_METHOD'] == 'POST':
            start_response(CONFLICT, TEXT_PLAIN)
            return KEY_ALREADY_EXISTS
        """

        meta = json.loads(metakey.decode('utf-8'))
        volume = meta['volume']

    # redirects
    headers = [('Location', 'http://%s%s' % (volume, key))]
    start_response(TEMPORARY_REDIRECT, headers)
    db.put(b'key-%d' % time.time(), b'bob')


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
        start_response(OK, TEXT_PLAIN)
        return [fc.get(hashkey)]

    if env['REQUEST_METHOD'] == 'POST':
        file_len = int(env.get('CONTENT_LENGTH', '0'))
        if file_len > 0:
            fc.post(hashkey, env['wsgi.input'].read(file_len))
            start_response(OK, TEXT_PLAIN)
            return [b'']
        else:
            start_response(LENGTH_REQUIRED, TEXT_PLAIN)
            return [b'']

    if env['REQUEST_METHOD'] == 'DELETE':
        fc.delete(hashkey)
