
```markdown
# User Management System API (Django REST Framework)
```
## Objective
Develop a User Management System API using Django REST Framework (DRF) with the following key features:
- **Custom User Model** (includes profile picture & role-based access)  
- **JWT Authentication** (with additional user information in the token)  
- **Role-Based Access Control (RBAC)**  
- **Welcome Email Notification**  


## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/hamzagill906/user_management_api.git
```

```sh
cd <user_management_api>
```

### 2. Install Dependencies (Using Pipenv)
```sh
pipenv install
```

### 3. Activate Virtual Environment
```sh
pipenv shell
```

### 4. Apply Migrations
```sh
python manage.py migrate
```

### 5. Run the Development Server
```sh
python manage.py runserver
```

## Task Overview & Implementation Details

### Custom User Model
Extend Django's default User model to include:
- `profile_picture` (ImageField)
- `role` (Admin, Editor, Viewer)
- Additional fields are added as needed like `id`,`email` etc.

### JWT Authentication with Additional User Data
- Implemented authentication using JWT tokens.
- Modify the JWT payload to include additional user details (e.g., `user_id`, `role`, URL).

### Role-Based Access Control (RBAC)
- **Admin**: Create, Update, Delete users
- **Editor**: Update users (but cannot change roles)
- **Viewer**: Only view user profiles
- Enforce RBAC in API endpoints.

### Send Welcome Email
- When a new user registers, send them a welcome email.
- Use Django's built-in email functionality.

### API Testing with Swagger
- To test the API using Swagger UI, navigate to `/swagger/` or `/docs/` (depending on your setup).
- **Before testing any secured endpoints**, first log in using the `/api/auth/login/` endpoint.
- Copy the **access token** from the login response.
- Click the **Authorize** button in Swagger.
- Enter the token in the format:  
```sh
Bearer <access_token>
```

## API Endpoints

### Authentication APIs

| Method | Endpoint             | Description                     | Permissions         |
|--------|----------------------|-------------------------------  |---------------------|
| POST   | `/api/auth/register/` | Register a new user            | Open to all         |
| POST   | `/api/auth/login/`    | Login and get JWT token        | Open to all         |
| POST   | `/api/auth/logout/`   | Logout user (invalidate token) | Authenticated users |
| POST   | `/api/auth/refresh/`  | Refresh Token                  | Authenticated users |

### User CRUD APIs (with RBAC enforcement)

| Method | Endpoint             | Description                  | Permissions                        |
|--------|----------------------|------------------------------|-----------------------------------|
| GET    | `/api/users/`        | List all users               | Admin & Viewer                   |
| GET    | `/api/users/<id>/`   | Retrieve user profile        | All roles                         |
| POST   | `/api/users/`        | Create a new user            | Admin only                        |
| PUT    | `/api/users/<id>/`   | Update user info             | Admin & Editor (Editor can’t change roles) |
| DELETE | `/api/users/<id>/`   | Delete a user                | Admin only                        |

## Additional Notes
- Implement **Swagger** for API documentation and testing.
- The core functionality must remain intact, but additional fields, structuring, or minor enhancements are allowed.
- POstman Collection also Provided for testing the API.

