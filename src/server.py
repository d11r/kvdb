import json
import os
import random
import requests

from src.constants import *
from src.file_cache import FileCache
from src.key_value import KeyValue


def resp(start_response, code, headers=TEXT_PLAIN, body=b''):
    start_response(code, headers)
    return body


# --- MASTER SERVER ---


if os.environ['TYPE'] == 'master':
    volumes = os.environ['VOLUMES'].split(',')

    for v in volumes:
        print(v)

    db = KeyValue(os.environ['DB'])


def master(env, start_response):
    host = env['SERVER_NAME'] + ":" + env['SERVER_PORT']
    key = env['PATH_INFO']

    if env['REQUEST_METHOD'] == 'PUT':
        # called by volume servers
        file_len = int(env.get('CONTENT_LENGTH', '0'))
        if file_len > 0:
            db.put(key.encode('utf-8'), env['wsgi.input'].read())
        else:
            db.delete(key.encode('utf-8'))
        return resp(start_response, OK)

    metakey = db.get(key.encode('utf-8'))

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
    headers = [('Location', 'http://%s%s?%s' % (volume, key, host))]
    return resp(start_response, TEMPORARY_REDIRECT, headers)


# --- VOLUME SERVER ---

if os.environ['TYPE'] == 'volume':
    # create file cache
    fc = FileCache(os.environ['VOLUME'])


def volume(env, start_response):
    host = env['SERVER_NAME'] + ":" + env['SERVER_PORT']
    key = env['PATH_INFO']

    print(env)

    if env['REQUEST_METHOD'] == 'POST':
        if fc.exists(key):
            req = requests.put('http://' + env['QUERY_STRING'] + key, json={'volume': host})
            return resp(start_response, CONFLICT)
        file_len = int(env.get('CONTENT_LENGTH', '0'))
        if file_len > 0:
            fc.post(key, env['wsgi.input'])
            req = requests.put('http://' + env['QUERY_STRING'] + key, json={'volume': host})
            if req.status_code == 200:
                return resp(start_response, CREATED)
            else:
                fc.delete(key)
                return resp(start_response, INTERNAL_SERVER_ERROR)

        else:
            return resp(start_response, LENGTH_REQUIRED)

    if env['REQUEST_METHOD'] == 'DELETE':
        req = requests.put("http://" + env['QUERY_STRING'] + key, data='')

        if req.status_code == 200:
            if fc.delete(key):
                return resp(start_response, OK)
            else:
                return resp(start_response, INTERNAL_SERVER_ERROR + ' - not on disk')
        else:
            return resp(start_response, INTERNAL_SERVER_ERROR + '(master db write fail)')

    if env['REQUEST_METHOD'] == 'GET':
        return resp(start_response, OK, body=fc.get(key).read())

    # key is not in cache, should return not found
    if not fc.exists(key):
        return resp(start_response, NOT_FOUND, body=KEY_NOT_FOUND)
