import sys
sys.path.append('..')
from app import create_app
from app.exts import db

import unittest

class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client(self)

        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()        
        db.create_all() # < --- update

    def tearDown(self):
        db.session.remove()
        db.drop_all() # < --- update        
        self.app_ctxt.pop()        
        self.app = None        
        self.app_ctxt = None 

if __name__ == '__main__':
    unittest.main()