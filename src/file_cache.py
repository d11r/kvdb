import os


class FileCache(object):
    def __init__(self, basedir):
        """ constructor for the file cache class """
        self.basedir = os.path.realpath(basedir)
        os.makedirs(self.basedir, exist_ok=True)

    def key_to_path(self, key, mkdir_is_ok=False):
        """ given a key returns a path that's 3 levels deep  """
        path = self.basedir + '/' + key[0:2] + '/' + key[0:4]
        if not os.path.isdir(path) and mkdir_is_ok:
            os.makedirs(path, exist_ok=True)
        return os.path.join(path, key)

    def exists(self, key):
        """ given a key returns if that key is already in cache  """
        return os.path.isfile(self.key_to_path(key))

    def post(self, key, value):
        """ given a key and a value insert them into the cache  """
        with open(self.key_to_path(key, True), 'wb') as f:
            f.write(value)

    def delete(self, key):
        """ given a key deletes the corresponding key-value pair from the cache """
        os.unlink(self.key_to_path(key))

    def get(self, key):
        """ given a key returns its corresponding value from the cache """
        return open(self.key_to_path(key), 'rb').read()
