import json
import os
import random
import hashlib

from src.constants import *
from src.file_cache import FileCache


def resp(start_response, code, headers=TEXT_PLAIN, body=b''):
    start_response(code, headers)
    return body


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

    if env['REQUEST_METHOD'] == 'POST':
        file_len = int(env.get('CONTENT_LENGTH', '0'))
        if file_len > 0:
            db.put(key.encode('utf-8'), env['wsgi.input'].read(), sync=True)
        else:
            db.delete(key.encode('utf-8'))
        return resp(start_response, OK)

    if metakey is None:
        if env['REQUEST_METHOD'] == 'POST':
            # handler for data insertion
            # TODO: volume selection should not be random
            volume = random.choice(volumes)
        else:
            return resp(start_response, NOT_FOUND)
    else:
        # key is found
        if env['REQUEST_METHOD'] == 'POST':
            return resp(start_response, CONFLICT)

        # store metakey in db
        meta = json.loads(metakey.decode('utf-8'))
        volume = meta['volume']

    # redirects
    headers = [('Location', 'http://%s%s' % (volume, key))]
    return resp(start_response, TEMPORARY_REDIRECT, headers)


# --- VOLUME SERVER ---

if os.environ['TYPE'] == 'volume':
    host = os.environ['HOST'] + ":" + os.environ['PORT']

    # create file cache
    fc = FileCache(os.environ['VOLUME'])


def volume(env, start_response):
    key = env['REQUEST_URI'].encode('utf-8')

    if env['REQUEST_METHOD'] == 'POST':
        if fc.exists(key):
            return resp(start_response, CONFLICT)

        file_len = int(env.get('CONTENT_LENGTH', '0'))
        if file_len > 0:
            fc.post(key, env['wsgi.input'])
            return resp(start_response, CREATED)
        else:
            return resp(start_response, LENGTH_REQUIRED)

    # key is not in cache, should return not found
    if not fc.exists(key):
        return resp(start_response, NOT_FOUND, body=KEY_NOT_FOUND)

    if env['REQUEST_METHOD'] == 'GET':
        return resp(start_response, OK, body=fc.get(key).read())

    if env['REQUEST_METHOD'] == 'DELETE':
        fc.delete(key)
        return resp(start_response, OK)
