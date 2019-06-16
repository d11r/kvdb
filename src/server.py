import sys
import os
print('----------------->>>', sys.argv, os.environ['TYPE'])

def master(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello, World!"]


def volume(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hi, World!"]
