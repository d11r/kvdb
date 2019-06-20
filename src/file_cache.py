import os
import hashlib
import tempfile


class FileCache(object):
    def __init__(self, basedir):
        """ constructor for the file cache class """
        self.basedir = os.path.realpath(basedir)
        self.tmpdir = os.path.join(self.basedir, 'tmp')
        os.makedirs(self.tmpdir, exist_ok=True)
        print("FileCache in %s" % basedir)

    def key_to_path(self, key, mkdir_is_ok=False):
        """ given a key returns a path that's 3 levels deep  """
        hashkey = hashlib.md5(key.encode('utf-8')).hexdigest()

        path = self.basedir + '/' + hashkey[0:2] + '/' + hashkey[0:4]
        if not os.path.isdir(path) and mkdir_is_ok:
            os.makedirs(path, exist_ok=True)
        return os.path.join(path, hashkey)

    def exists(self, key):
        """ given a key returns if that key is already in cache  """
        return os.path.isfile(self.key_to_path(key))

    def post(self, key, stream):
        """ given a key and a value insert them into the cache  """
        with tempfile.NamedTemporaryFile(dir=self.tmpdir, delete=False) as f:
            # TODO: make writing to a file more efficient (do not waste RAM)
            f.write(stream.read())
            import xattr
            xattr.setxattr(f.name, 'user.key', key.encode('utf-8'))
            os.rename(f.name, self.key_to_path(key, True))

    def delete(self, key):
        """ given a key deletes the corresponding key-value pair from the cache """
        try:
            os.unlink(self.key_to_path(key))
            return True
        except FileNotFoundError:
            pass
        return False

    def get(self, key):
        """ given a key returns its corresponding value from the cache """
        return open(self.key_to_path(key), 'rb')
