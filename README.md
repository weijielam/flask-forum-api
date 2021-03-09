# Flask/React Forum

## Deployment
### Authentication when using live deployment
For testing the live deployment, a Postman collection with access tokens is provided for convenience
## Testing
## Style Guide
The source follows PEP8. Please use `pycodestyle` for guidance:
```
pycodestyle --exclude=env
```
## Endpoints
### `GET /`
The only public endpoint, for debugging. Returns: "Healthy"

### `GET /categories`
### `GET /posts`
### `POST /categories`
## Authentication and Permissions
Authentication is handled via Auth0.