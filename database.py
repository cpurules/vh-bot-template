import json
import os.path

from pyArango.connection import *

class Database:
    def __init__(self, file='dbconfig.json'):
        if not os.path.exists(file):
            raise FileNotFoundError('Could not find configuration file: ' + file)

        with open(file) as f:
            try:
                config_dict = json.load(f)
            except Exception as e:
                raise Exception('Error while parsing ' + file + ': ' + e)
        
        required_fields = ['DB_SERVER', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_DATABASE']
        for field in required_fields:
            if not field in config_dict:
                raise KeyError('Missing field from ' + file + ': ' + field)
            if not config_dict[field]:
                raise ValueError('No value specified for field ' + field)
        
        arangoURL = 'http://{0}:{1}'.format(config_dict['DB_SERVER'], config_dict['DB_PORT'])
        try:
            conn = Connection(arangoURL=arangoURL, username=config_dict['DB_USER'], password=config_dict['DB_PASS'])
        except Exception:
            raise RuntimeError('Unable to connect to ArangoDB on {0}.  Please verify the server and logon settings'.format(arangoURL))
        
        if not config_dict['DB_DATABASE'] in conn.databases:
            conn.createDatabase(name=config_dict['DB_DATABASE'])

        self.db = conn[config_dict['DB_DATABASE']]

        collections = []

        for collection in collections:
            if not self.db.hasCollection(collection):
                self.db.createCollection(name=collection)
                self.db.reloadCollections()
        
        # self._collection = self.db['Collection']
    