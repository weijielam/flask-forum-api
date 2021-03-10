import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, \
     Post, Category, Comment
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)

    # this needs to be run once to create the database
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

    @app.route('/categories')
    @requires_auth("get:categories")
    def get_categories(payload):
        try:
            categories_query = Category.query.order_by(Category.id).all()
            categories = [category.short() for category in categories_query]
        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "categories": categories
        }), 200

    @app.route('/categories', methods=['POST'])
    @requires_auth("post:categories")
    def create_category(payload):
        try:
            data = request.get_json()
            name = data['name']
            description = data['description']
            category = Category(name, description)
            category.insert()

        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "created_category_id": category.id
        }), 200

    @app.route('/categories/<int:id>', methods=['PATCH'])
    @requires_auth("patch:categories")
    def update_category(payload, id):
        try:
            data = request.get_json()
            category = Category.query.filter_by(id=id).one_or_none()

            if (category is None):
                abort(404)

            description = data['description']
            category.description = description
            category.update()

        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "category": category.long()
        }), 200

    @app.route('/posts')
    @requires_auth("get:posts")
    def get_posts(payload):
        try:
            posts_query = Post.query.order_by(Post.id).all()
            posts = [post.short() for post in posts_query]
        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "posts": posts
        }), 200

    @app.route('/posts/<int:id>', methods=['GET'])
    @requires_auth("get:posts")
    def get_post_by_id(payload, id):
        try:
            post = Post.query.get(id)
            comments_query = Comment.query.order_by(Comment.post_id == id)
            comments = [comment.long() for comment in comments_query]
        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "post": [post.long()],
            "comments": comments
        })

    @app.route('/categories/<int:id>', methods=['GET'])
    @requires_auth("get:posts")
    def get_posts_from_category_id(payload, id):
        try:
            category_query = Category.query.get(id)
            category = category_query.long()
            posts_query = Post.query.join(Category)\
                .filter(Post.category_id == id).all()
            posts = [post.short() for post in posts_query]
        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "category": category,
            "posts": posts
        })

    @app.route('/posts', methods=['POST'])
    @requires_auth("post:posts")
    def create_post(payload):
        try:
            data = request.get_json()

            title = data['title']
            body = data['body']
            category_id = data['category_id']

            post = Post(title, body, category_id)
            post.insert()

        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "created_post_id": post.id
        }), 200

    @app.route('/posts/<int:id>', methods=['DELETE'])
    @requires_auth("delete:posts")
    def delete_post(payload, id):
        post = Post.query.filter_by(id=id).one_or_none()
        if post is None:
            abort(404)
        try:
            post.delete()
        except Exception as e:
            abort(422)
        return jsonify({'success': True, 'delete': id}), 200

    @app.route('/comments', methods=['POST'])
    @requires_auth("post:comments")
    def create_comment_on_post(payload):
        try:
            data = request.get_json()
            post_id = data['post_id']
            body = data['body']
            comment = Comment(post_id, body)
            comment.insert()

        except Exception as e:
            abort(422)

        return jsonify({
            "success": True,
            "post_id": comment.post_id,
            "created_comment_id": comment.id
        })

    @app.route('/comments', methods=['DELETE'])
    @requires_auth("delete:comments")
    def delete_comment_on_post(payload):
        try:
            data = request.get_json()
            comment_id = data['comment_id']
            comment = Comment.query.filter_by(id=comment_id).one_or_none()
            id = comment.id

            if comment is None:
                abort(404)
            try:
                comment.delete()
            except Exception as e:
                abort(422)
            return jsonify({'success': True, 'delete': id}), 200

        except Exception as e:
            abort(400)

        return jsonify({
            "success": True,
            "deleted": id
        })

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(422)
    @app.errorhandler(500)
    def error_handler(error):
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
