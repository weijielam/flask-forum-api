import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import (
    setup_db, db_drop_and_create_all, Post, Comment, Category
)
# Enabling Auth0 if it was disabled before
# NOTE: Please run these tests in moderation
# to not get rate-limited by Auth0 servers
if os.environ.get("DISABLE_AUTH0"):
    del os.environ["DISABLE_AUTH0"]

USER_TOKEN = os.environ["USER_TOKEN"]
ADMIN_TOKEN = os.environ["ADMIN_TOKEN"]

USER_HEADERS = {"Authorization": "Bearer {}".format(USER_TOKEN)}
ADMIN_HEADERS = {"Authorization": "Bearer {}".format(ADMIN_TOKEN)}


class ForumTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "forum_test"
        self.database_path = "postgres://{}/{}" \
            .format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # db_drop_and_create_all()

        self.VALID_NEW_CATEGORY = {
            "name": "RBAC Test Category",
            "description": "This is a RBAC Test Category description."
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
            "id": 1
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

    # ADMIN TESTS
    def test_admin_create_category(self):
        response = self.client() \
            .post('/categories',
                  json=self.VALID_NEW_CATEGORY, headers=ADMIN_HEADERS)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('created_category_id', data)

    def test_admin_update_category(self):
        response = self.client() \
            .patch('/categories/1',
                   json=self.VALID_UPDATE_CATEGORY, headers=ADMIN_HEADERS)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('category', data)
        self.assertEqual(
            data["category"]["description"],
            self.VALID_UPDATE_CATEGORY["description"])

    # PUBLIC TESTS
    def test_public_health(self):
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'Running!')

    def test_public_get_categories_401(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertIn('code', data)

    # USER TESTS
    def test_user_get_categories(self):
        response = self.client().get('/categories', headers=USER_HEADERS)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('categories', data)
        self.assertTrue(len(data["categories"]))

    def test_user_get_posts(self):
        response = self.client().get('/posts', headers=USER_HEADERS)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('posts', data)

    def test_user_create_category_401(self):
        response = self.client() \
            .post('/categories',
                  json=self.VALID_NEW_CATEGORY, headers=USER_HEADERS)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
