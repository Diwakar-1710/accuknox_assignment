# Django REST API for User Authentication and Friend Management

This Django project provides a set of APIs for user authentication and managing friend requests. It includes functionality for user signup, login, searching for users, sending friend requests, responding to friend requests, retrieving a list of friends, and managing pending friend requests.

# Postman Documentaion Link

You can find the Postman documentation linked below, where each API has been thoroughly tested.
(https://documenter.getpostman.com/view/16764987/2sA3Qy4oG4)

## Features

- User signup: Register new users with email and password.
- User login: Authenticate users and generate JWT tokens for authentication.
- User search: Search for users by email or username.
- Friend requests: Send and respond to friend requests.
- Friend list: Retrieve a list of friends for a given user.
- Pending requests: Retrieve pending friend requests for a user.
- All friend requests: Retrieve all friend requests in the system.

## Installation

1. **Clone the Repository:**
   ```
   git clone <repository_url>
   cd social_network
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   - By default, the project uses SQLite as the database, which doesn't require any additional setup. The SQLite database file (`db.sqlite3`) will be created automatically.
   - If you want to use a different database like PostgreSQL or MySQL, make appropriate changes to the `DATABASES` setting in the `settings.py` file.

4. **Run Migrations:**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Optional):**
   ```
   python manage.py createsuperuser
   ```

6. **Run the Development Server:**
   ```
   python manage.py runserver
   ```

7. **Access the APIs:**
   - The development server should now be running locally. You can access the APIs using the following endpoints:
     - Signup: POST `/api/signup/`
     - Login: POST `/api/login/`
     - Search User: GET `/api/search_user/?query=<search_query>`
     - Send Friend Request: POST `/api/send_friend_request/`
     - Respond to Friend Request: POST `/api/respond_friend_request/`
     - Friend List: GET `/api/friend_list/`
     - Pending Requests: GET `/api/pending_requests/`
     - All Friend Requests: GET `/api/all_friend_requests/`
     
**Note:** Ensure that the appropriate authentication tokens are included in the headers of the requests requiring authentication. The JWT token obtained upon successful login should be included in the `Authorization` header as `Bearer <token>` for authenticated requests.

## Technologies Used

- Django
- Django REST Framework
- SQLite 

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.


...
