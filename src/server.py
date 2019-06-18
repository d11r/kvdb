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

class FileCache(object):
    def __init__(self, basedir):
        os.makedirs(basedir)
        self.basedir = basedir

    def key_to_path(self, key):
        """ given a key returns a path that's 2 levels deep (nginx)  """
        path = self.basedir + '/' + key[0:1] + '/' + key[1:2]
        if not os.path.isdir(path):
            os.makedirs(path)
        return os.path.join(path, key[2:])

    def exists(self, key):
        """ given a key returns if that key is already in cache  """
        return os.path.isfile(self.key_to_path(key))

    def put(self, key, value):
        """ given a key and a value insert them into the cache  """
        with open(self.key_to_path(key), 'wb') as f:
            f.write(value)

    def delete(self, key):
        """ given a key deletes the corresponding key-value pair from the cache """
        os.path.unlink(self.key_to_path(key))

    def get(self, key):
        return open(self.key_to_path(key), 'rb').read()

if os.environ['TYPE'] == 'volume':
    import socket
    host = socket.gethostname()
    
    # register with master
    master = os.environ['MASTER']
    
    # create file cache
    fc = FileCache(os.environ['VOLUME'])

def volume(env, start_response):
    key = env['REQUEST_URI'].encode('utf-8')
    haskey = hashlib.md5(key).hexdigest()

    if not fc.exists(hashkey):
        pass 
