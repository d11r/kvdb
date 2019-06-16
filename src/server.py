import sys
import os
import time

print('----------------->>>', sys.argv, os.environ['TYPE'], os.getpid())

if os.environ['TYPE'] == 'master':
    import plyvel 
    db = plyvel.DB(os.environ['DB'], create_if_missing=True)

def master(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    print(os.getpid())
    db.put(b'key-%d' % time.time(), b'bob')
    return [b"Hello, World!"]


def volume(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hi, World!"]
