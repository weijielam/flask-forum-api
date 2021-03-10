# Flask Forum API

## Capstone Project for Udacity's Full Stack Developer Nanodegree
Heroku Link: https://flask-forum-app-api.herokuapp.com/

While running locally: http://localhost:5000

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


## Running the server
Before running the application locally, make the following changes in the `app.py` file in the root directory
### Authentication when using live deployment
For testing the live deployment, a Postman collection with access tokens is provided for convenience
## Testing
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
- 401
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
### `GET /posts`
- Returns the list of posts
- Required Headers:
    - `Authorization` header with bearer token that has `get:posts` permission.
- Request arguments: None
- Returns: 
    - `200 OK` response, body with a 

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
            "title": "Who let the dogs out?"
        }
    ],
    "success": true
}
```
### `GET /posts/<int:id>
- Returns post by id
- Required Headers:
    - `Authorization` header with bearer token that has `get:posts` permission.
- Request arguments: int id
- Returns: 
    - `200 OK` response, body with a 

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
            "title": "Who let the dogs out?"
        }
    ],
    "success": true
}
```

### `POST /categories`
### `POST /posts`
### `POST /commments/`

### `UPDATE /categories/<int:id>`

### `DELETE /posts/<int:id>`
### `DELETE /comments/`

## Authentication and Permissions
Authentication is handled via Auth0.

## Testing
For testing the backend, run the following commands (in the exact order):
```bash
dropdb forum_test
createdb forum_test
python test_app.py
python test_rbac.py
```