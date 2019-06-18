import os


class FileCache(object):
    def __init__(self, basedir):
        """ constructor for the file cache class """
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
        # TODO: fix unlink problem
        os.path.unlink(self.key_to_path(key))

    def get(self, key):
        """ given a key returns its corresponding value from the cache """
        return open(self.key_to_path(key), 'rb').read()
