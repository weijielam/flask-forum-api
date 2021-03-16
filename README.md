# Flask Forum API
The Flask Forum API supports a basic web forum by allowing users to create posts on forum categories and comment on posts. There are two different user roles (and related permissions), which are:
- Registered User: Can view posts + categories, create posts and comment on posts.
- Admin: Same as above, can create categories, delete posts and comments.

## Capstone Project for Udacity's Full Stack Developer Nanodegree
Heroku Link: https://flask-forum-app-api.herokuapp.com/

While running locally: http://localhost:5000

## Motivation
This is my capstone project submission for the Udacity Full-Stack Developer Nanodegree program.

The goal is to demonstrate the ability to:

- Design data models and their relations using SQLAlchemy.
- Write database queries using SQLAlchemy.
- Design an HTTP API with Flask.
- Document the API and development guide in detail.
- Implement authentication and Role Based Access Control using Auth0.
- Test the API and access control capabilities.
- Provide PEP8 compliant, and readable code.
- Deploy the app to Heroku.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

It is recommend to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- PostgreSQL, also known as Postgres, is a free and open-source relational database management system

- [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) is used to manage any changes made to the models and handle database migrations

- [Flask CORS](https://flask-cors.readthedocs.io/en/latest/) a Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.

- [Auth0](https://auth0.com/) is used to provide RBAC functionality by providing JWT tokens for permissions

- [Python Unittest](https://docs.python.org/3/library/unittest.html) is used to test the application functionality and RBAC permissions

- Postman - Used to test live deployment endpoints of the application

## Database Setup
With Postgres running, initialize the the database
```
dropdb forum
createdb forum
```
## Running the server
Before running the application locally, make the following changes in the `app.py` file in the root directory
- Uncomment the line `db_drop_and_create_all()` on the initial run to setup the required tables in the database

To run the server, execute:

```bash
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py
flask run --reload
```

Setting the `FLASK_APP` variable to app.py directs flask to use the `app.py` file to find the application

Using the `--reload` flag will detect file changes and restart the server automatically.

### Authentication when using live deployment
For testing the live deployment, a Postman collection with access tokens is provided for convenience.

## Style Guide
The source follows PEP8. Please use `pycodestyle` for guidance:
```
pycodestyle --exclude=env
```

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "The requested URL was not found on the server."
    "success": false
}
```

The API will return the following errors based on how the request fails:
 - 400: Bad Request
 - 401: Unauthorized
 - 403: Forbidden
 - 404: Not Found
 - 405: Method Not Allowed
 - 422: Unprocessable Entity
 - 500: Internal Server Error

## Endpoints

### `GET /`
The only public endpoint, for debugging. Returns: `"Healthy"`

### `GET /categories`
- Returns the list of categories
- Required Headers:
    - `Authorization` header with bearer token that has `get:categories` permission.
- Request arguments: None
- Returns:
    - `200 OK` response, body with a `categories` key, its value being the list of categories

```
{
    "categories": [
        {
            "id": 1,
            "name": "Programming"
        }
    ],
    "success": true
}
```
### `GET /categories/<int:id>`
- Returns a category and the list of posts in the category
- Required Headers:
    - `Authorization` header with bearer token that has `get:categories` permission. 
- Request arguments: Category ID, included as a parameter following a forward slash (/)
- Returns:
    - `200 OK` response, body with a category and list of posts.

```
{
    "category": {
        "description": "A place to discuss coding",
        "id": 1,
        "name": "Programming"
    },
    "posts": [
        {
            "created_timestamp": "Thu, 11 Mar 2021 21:56:03 GMT",
            "id": 1,
            "title": "Why am I bad at coding"
        },
        {
            "created_timestamp": "Thu, 11 Mar 2021 21:56:05 GMT",
            "id": 2,
            "title": "Is copying code from Stack Overflow for my startup legal?"
        }
    ],
    "success": true
}
```
### `GET /posts`
- Returns a list of posts
- Required Headers:
    - `Authorization` header with bearer token that has `get:posts` permission.
- Request arguments: None
- Returns: 
    - `200 OK` response, body with a `posts` key, its value being the list of posts

```
{
    "posts": [
        {
            "created_timestamp": "Mon, 08 Mar 2021 23:06:47 GMT",
            "id": 1,
            "title": "Can someone review my API documentation?"
        },
        {
            "created_timestamp": "Mon, 08 Mar 2021 23:13:09 GMT",
            "id": 2,
            "title": "How do I get posts from this API?"
        }
    ],
    "success": true
}
```
### `GET /posts/<int:id>
- Returns an existing posts and it's comments
- Required Headers:
    - `Authorization` header with bearer token that has `get:posts` permission.
- Request arguments: Post id
- Returns: 
    - `200 OK` response, body with a 

```
{
    "comments": [
        {
            "body": "Here we go",
            "created_timestamp": "Thu, 11 Mar 2021 21:56:09 GMT",
            "id": 1,
            "post_id": 1
        },
        {
            "body": "I don't know what's updog",
            "created_timestamp": "Thu, 11 Mar 2021 21:56:10 GMT",
            "id": 2,
            "post_id": 1
        },
        {
            "body": "What's updog?",
            "created_timestamp": "Thu, 11 Mar 2021 21:56:11 GMT",
            "id": 3,
            "post_id": 1
        }
    ],
    "post": [
        {
            "body": "Thoughts on the updog protocol?",
            "category_id": 2,
            "created_timestamp": "Thu, 11 Mar 2021 21:56:03 GMT",
            "id": 1,
            "title": "Valid New Post"
        }
    ],
    "success": true
}
```

### `POST /categories`
- Adds a new category
- Required headers:
    `Authorization` header with bearer token that has `post:categories` permission.
- Request body:
    - `name`: Category name string. Must be unique.
    - `description`: Category description string. Optional.
- Returns:
    - `200 OK` response when a new record was successfully created. `422 Unprocessable` response when `name` is missing or already exists.

```
{
    "created_category_id": 3,
    "success": true
}
```
### `POST /posts`
- Adds a new post
- Required headers:
    `Authorization` header with bearer token that has `post:posts` permission.
- Request body:
    - `title`: Post title string. Required.
    - `body`: Post body string. Optional.
    - `category_id`: Post category id integer. Required.
- Returns:
    - `200 OK` response when a new record was successfully created. `422 Unprocessable` response when required fields are missing or not valid.

```
{
    "created_post_id": 2,
    "success": true
}
```

### `POST /commments/`
- Adds a new comment
- Required headers:
    `Authorization` header with bearer token that has `post:comments` permission.
- Request body:
    - `post_id`: Post id integer. Required.
    - `body`: Post body string. Required.
- Returns:
    - `200 OK` response when a new record was successfully created. `422 Unprocessable` response when required fields are missing or not valid.

```
{
    "created_comment_id": 3,
    "post_id": 1,
    "success": true
}
```

### `PATCH /categories/<int:id>`
- Updates the description for a category
- Required Headers:
    - `Authorization` header with bearer token that has `update:categories` permission.
- Request arguments: category id int
- Request Body: 
    - `description`: Category description string.
- Returns:
    `200 OK` response when the description was successfully updated. `422 Unprocessable` response when required fields are missing or invalid.

```
{
    "category": {
        "description": "Please don't post about updog",
        "id": 1,
        "name": "Programming"
    },
    "success": true
}
```

### `DELETE /posts/<int:id>`
- Deletes a post and related comments
- Required Headers:
    - `Authorization` header with bearer token that has `delete:posts` permission.
- Request arguments: post id int
- Returns:
    `200 OK` response when the description was successfully updated. `404` when post id is invalid.

```
{
    "delete": 3,
    "success": true
}
```


### `DELETE /comments/`
- Deletes a comment
- Required Headers:
    - `Authorization` header with bearer token that has `delete:comments` permission.
- Request arguments: none
- Request Body:
    - `id`: Comment id int

```
{
    "delete": 1,
    "success": true
}
```
## Authentication and Permissions
Authentication is handled via Auth0.

All except one endpoints require authentication, and proper permission. The root is a public endpoint left there for debugging.

The app currently does not offer a frontend with a login.

## Testing
For testing the backend, run the following commands (in the exact order):
```bash
dropdb forum_test
createdb forum_test
python test_app.py
. ./setup.sh        # export USER and ADMIN token
python test_rbac.py
```
