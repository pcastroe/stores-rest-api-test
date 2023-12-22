import app

from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        # initielize client
        with self.app() as client:
            # because our methods save things to database we also need to initialize the db
            with self.app_context():
                # we use formdata type (includes every field as if we have filled a form
                # that's fine for our user resource because we don't specify where to look
                # by default it looks at the forms first
                response = client.post('/register',data={'username':'test','password':'1234'})

                self.assertEqual(response.status_code,201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))
                # request.data is a dictionary that gets converted into json when the request gets sent
                # so we need to make sure to convert it back from a json object into a python dictionary
                # json.loads() is used to parse a JSON string into a Python object,
                # while jsonify() is used to create a JSON response from a Python object

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                # '/auth' endpoint requires that we send the data in json format
                # json.dumps converts a Python dictionary into a JSON string
                auth_response = client.post('/auth',
                                           data=json.dumps({'username':'test','password':'1234'}),
                                           headers={'Content-Type':'application/json'})
                #Content-Type is a very common header to tell a web server what type of data we're sending

                #checks that the access token string is in the list of keys
                #when we authenticate, we get back an access token
                #whenever our app requires that we are logged in, we are going to send this token
                #to the endpoint, and flask-jwt is going to do the verification for us
                self.assertIn('access_token',json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code,400)
                self.assertDictEqual({'message':'A user with that username already exists'},
                                     json.loads(response.data))

