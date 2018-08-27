import xmlrpc.client as xc

class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = None
        self.uid = None
        self.models = None

    def connect(self):
        try:
            self.common = xc.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            self.models = xc.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            return self.models
        except:
            return "error in connection"

    def getInfo(self):
        self.connect()
        print("Common Version: ", self.common.version(), "\n")
        print("User Id : ", self.uid, "\n")

    def create(self, model_name, values):
        try:
            self.connect()
            id = self.models.execute_kw(self.db, self.uid, self.password, model_name, 'create', [values])
            return id
        except:
            print( "Not Inserted!")
            self.models.execute_kw(self.db, self.uid, self.password, 'res.partner', 'unlink', [[7]])

    def delete(self, model_name, ids):
        try:
            self.connect()
            self.models.execute_kw(self.db, self.uid, self.password, model_name, 'unlink', [ids])
            return "Deleted"
        except:
            return "Not Deleted!"

    def update(self, model_name, ids, values):
        try:
            self.connect()
            print(self.models.execute_kw(self.db, self.uid, self.password, model_name, 'write', [ids, values]))
            return "Updated"
        except:
            return "Not Updated!"

    def get(self, model_name, ids):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'name_get', [ids])

        except:
            return "Not Founded!"

    def read(self, model_name, ids, fields):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'read', [ids],
                                          {'fields': fields})

        except:
            return "Not Founded!"

    def getFields(self, model_name, attributes):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'fields_get', [],
                                          {'attributes': attributes})

        except:
            return "Empty!"

    def search(self, model_name, params):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'search', [params])

        except:
            return "Empty!"

    def search_limit(self, model_name, params, offset=0, limit=1):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'search', [params],
                                          {'offset': offset, 'limit': limit})

        except:
            return "Empty!"

    def search_count(self, model_name, params):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'search_count', [params])

        except:
            return "Empty!"

    def search_read(self, model_name, params, fields):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'search_read', [params],
                                          {'fields': fields})

        except:
            return "Empty!"

    def search_read_limit(self, model_name, params, fields, offset=0, limit=1):
        try:
            self.connect()
            return self.models.execute_kw(self.db, self.uid, self.password, model_name, 'search_read', [params],
                                          {'fields': fields, 'offset': offset, 'limit': limit})

        except:
            return "Empty!"