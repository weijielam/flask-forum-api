import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Post, Category, User, Comment
from datetime import datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)

    db_drop_and_create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    @app.route('/')
    def health():
        return jsonify({'health': 'Running!'}), 200

    # Get all posts 
    @app.route('/posts')
    def get_posts():
        posts_query = Post.query.order_by(Post.id).all()
        posts = [post.short() for post in posts_query]

        return jsonify({
            "success": True,
            "posts": posts
        }), 200

    @app.route('/posts', methods=['POST'])
    def create_post():
        try:
            new_post = Post("title","body",str(datetime.now()), 1,1)
            new_post.insert()
        except Exception as e:
            print(e)
        return jsonify({
                "success": True,
                "created_post_id": new_post.id
            }), 201

    # Get all categories
    @app.route('/categories')
    def categories():
        categories_query = Category.query.order_by(Category.id).all()
        categories = [category.short() for category in categories_query]

        return jsonify({
            "success": True,
            "posts": categories
        }), 200

    # Get all users (this will require auth permissions)
    @app.route('/users')
    def users():
        users_query = User.query.order_by(User.id).all()
        users = [user.short() for user in users_query]

        return jsonify({
            "success": True,
            "posts": users
        }), 200


    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

