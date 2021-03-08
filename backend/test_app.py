import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from database.models import setup_db, db_drop_and_create_all, Post, Comment, Category

# PYTHON UNIT TESTS ARE RAN IN ALPHABETICAL ORDER! 

# Disabling Auth0 calls when testing core functionality
os.environ["DISABLE_AUTH0"] = "1"

class ForumTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "forum_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # db_drop_and_create_all()
    
        self.VALID_NEW_CATEGORY = {
            "name": "Valid Test Category",
            "description": "This is a Test Category description."
        }

        self.INVALID_NEW_CATEGORY = {
            "name": ""
        }

        self.VALID_UPDATE_CATEGORY = {
            "description": "This is an updated Category description"
        }

        self.INVALID_UPDATE_CATEGORY = {
            "name": "This will not work"
        }

        self.VALID_NEW_POST = {
            "title": "Valid New Post",
            "body": "This is a new test Post.",
            "category_id": 1
        }

        self.INVALID_NEW_POST = {
            "body": "This Post is invalid",
            "category_id": 1
        }

        self.VALID_NEW_COMMENT = {
            "post_id": 1,
            "body": "This is a Valid Comment"
        }

        self.INVALID_NEW_COMMENT = {
            "body": "This Comment is invalid"
        }

        self.VALID_DELETE_COMMENT = {
            "comment_id": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()
        
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    """
    NOTE: unittest by default is ran in alphabetical order
    To get around an issue with test failing due to dependencies
    on previous test, the tests have alphanumeric prefix which 
    allows them to be ran in a specific order. At a later point 
    I may change the tests to work independently of each other.
    See: https://stackoverflow.com/questions/5387299/python-unittest-testcase-execution-order/5387956#5387956
    """
    def test_a_01_health(self):
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'Running!')

    def test_a_02_create_category(self):
        response = self.client().post('/categories', json=self.VALID_NEW_CATEGORY)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('created_category_id', data)

    def test_a_03_create_category_422(self):
        response = self.client().post('/categories', json=self.INVALID_NEW_CATEGORY)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_a_04_create_post(self):
        response = self.client().post('/posts', json=self.VALID_NEW_POST)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('created_post_id', data)

    def test_a_05_create_post_422(self):
        response = self.client().post('/posts', json=self.INVALID_NEW_POST)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_a_06_create_comment(self):
        response = self.client().post('/comments', json=self.VALID_NEW_COMMENT)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('created_comment_id', data)

    def test_a_07_create_comment_422(self):
        response = self.client().post('/comments', json=self.INVALID_NEW_COMMENT)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_b_01_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('categories', data)
        self.assertTrue(len(data["categories"])) 

    def test_b_02_get_posts(self):
        response = self.client().get('/posts')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('posts', data)

    def test_b_03_get_post_from_categories(self):
        response = self.client().get('/categories/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('category', data)
        self.assertIn('posts', data)

    def test_b_03_get_post_from_id(self):
        response = self.client().get('/posts/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])

    def test_c_01_update_category(self):
        response = self.client().patch('/categories/1', json=self.VALID_UPDATE_CATEGORY)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('category', data)
        self.assertEqual(data["category"]["description"], self.VALID_UPDATE_CATEGORY["description"])

    def test_c_02_update_category_404(self):
        response = self.client().patch('/categories/100', json=self.INVALID_UPDATE_CATEGORY)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertIn('message', data)
    
    def test_d_01_delete_comment_on_post(self):
        response = self.client().delete('/comments', json=self.VALID_DELETE_COMMENT)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('delete', data)

    def test_d_02_delete_post(self):
        response = self.client().delete('/posts/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('delete', data)

    def test_d_03_delete_post_404(self):
        response = self.client().delete('/posts/10000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()