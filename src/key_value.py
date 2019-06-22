class KeyValue(object):
    """
    uses levelDB to store keys and values
    TODO: in future, use multi-process-compatible DB
    """

    def __init__(self, func):
        """ creates a db if it doesn't already exist """
        import plyvel
        self.db = plyvel.DB(func, create_if_missing=True)

    def get(self, key):
        """ get the value that corresponds to the key given """
        return self.db.get(key)

    def put(self, key, value):
        """ puts the key-value pair to the DB """
        self.db.put(key, value)

    def delete(self, key):
        """ deletes the key-value pair from the DB """
        self.db.delete(key)
