import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Post, Category, User, Comment
# from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)

    # db_drop_and_create_all()

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
            data = request.get_json()

            title = data['title']
            body = data['body']
            category = data['category_id']

            post = Post(title, body, category)
            post.insert()

        except Exception as e:
            print(e)
            abort(400)

        return jsonify({
                "success": True,
                "created_post_id": post.id
            }), 200

    @app.route('/posts/<int:id>', methods=['DELETE'])
    def delete_post(payload, id):
        post = Post.query.filter_by(id=id).one_or_none()
        if post is None:
            abort(404)
        try:
            post.delete()
        except Exception as e:
            abort(400)
        return jsonify({'success': True, 'delete': id}), 200


    # CATEGORIES
    @app.route('/categories')
    def get_categories():
        categories_query = Category.query.order_by(Category.id).all()
        categories = [category.short() for category in categories_query]

        return jsonify({
            "success": True,
            "categories": categories
        }), 200

    @app.route('/categories', methods=['POST'])
    def create_category():
        try:
            data = request.get_json()

            category = Category('a', 'b')
            category.name = data['name']
            category.description = data['description']

            category.insert()

        except Exception as e:
            print(e)
            abort(400)

        return jsonify({
            "success": True,
            "created_category_id": category.id
        }), 200

    @app.route('/categories/<int:id>', methods=['PATCH'])
    def update_category(payload, id):
        try:
            data = request.get_json()
            category = Category.query.filter_by(id=id).one_or_none()

            if (category is None):
                abort(404)

            category.description = data['description']
            category.update()

        except Exception as e:
            abort(400)

        return jsonify({
            'success': True,
            'categories': [category.long()]
        }), 200

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

