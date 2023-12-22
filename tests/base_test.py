"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    # runs once for each TestCase
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        #una solución al bug al poner solamente db.init_app(app)
        #app.config['DEBUG'] = False
        #app.config['PROPAGATE_EXCEPTIONS'] = True     #this makes it so that if any exceptions occur they are sent to app.errorhandler
                                                       #this is set automatically as True if we define app.config['DEBUG'] to True
        #otra solución al bug al poner solamente db.init_app(app)
        with app.app_context():
            if "sqlalchemy" not in app.extensions:
                db.init_app(app)
            #db.init_app(app)

    # runs once for every test method
    def setUp(self):
        # Make sure database exists
        with app.app_context():
            db.create_all()
        # Get a test client
        # removed () from test_client so it creates a new test_client every test
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
