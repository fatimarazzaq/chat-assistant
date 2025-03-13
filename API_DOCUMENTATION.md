# API Documentation

## Web Routes

### Authentication
1. **Registration Page**
   - URL: `/accounts/register/`
   - Method: GET
   - Response: HTML registration form

2. **Login Page**
   - URL: `/accounts/login/`
   - Method: GET
   - Response: HTML login form

3. **Logout**
   - URL: `/accounts/logout/`
   - Method: GET
   - Response: Redirects to login page

### Chat Interface
1. **Chat Home**
   - URL: `/`
   - Method: GET
   - Response: HTML chat interface

2. **Create Chat Session**
   - URL: `/chat/session/create/`
   - Method: POST
   - Response: JSON
   ```json
   {
       "success": true,
       "session_id": "uuid",
       "session_title": "New Chat"
   }
   ```

3. **Rename Chat Session**
   - URL: `/chat/session/<uuid:session_id>/rename/`
   - Method: POST
   - Request Body:
   ```json
   {
       "title": "New Title"
   }
   ```
   - Response: JSON
   ```json
   {
       "success": true
   }
   ```

4. **Delete Chat Session**
   - URL: `/chat/session/<uuid:session_id>/delete/`
   - Method: DELETE
   - Response: JSON
   ```json
   {
       "success": true
   }
   ```

5. **Load Chat Session**
   - URL: `/load_session/<uuid:session_id>/`
   - Method: GET
   - Response: JSON
   ```json
   {
       "chats": [
           {
               "id": 1,
               "message": "Hello",
               "response": "Hi there!",
               "created_at": "2024-03-13T10:00:00Z"
           }
       ]
   }
   ```

6. **View Chat Session**
   - URL: `/chat/<uuid:session_id>/`
   - Method: GET
   - Response: HTML chat interface with loaded session

## API Routes (v1)

### Authentication API
1. **Register**
   - URL: `/api/v1/auth/register/`
   - Method: POST
   - Request Body:
   ```json
   {
       "username": "newuser",
       "email": "user@example.com",
       "password": "password123",
       "confirm_password": "password123"
   }
   ```
   - Response: JSON
   ```json
   {
       "user": {
           "id": 1,
           "username": "newuser",
           "email": "user@example.com"
       },
       "refresh": "refresh_token_here",
       "access": "access_token_here",
       "message": "User registered successfully"
   }
   ```

2. **Login**
   - URL: `/api/v1/auth/login/`
   - Method: POST
   - Request Body:
   ```json
   {
       "username": "newuser",
       "password": "password123"
   }
   ```
   - Response: JSON
   ```json
   {
       "user": {
           "id": 1,
           "username": "newuser",
           "email": "user@example.com"
       },
       "refresh": "refresh_token_here",
       "access": "access_token_here",
       "message": "Login successful"
   }
   ```

3. **Logout**
   - URL: `/api/v1/auth/logout/`
   - Method: POST
   - Headers: `Authorization: Bearer <access_token>`
   - Request Body:
   ```json
   {
       "refresh": "refresh_token_here"
   }
   ```
   - Response: JSON
   ```json
   {
       "message": "Logout successful"
   }
   ```

4. **User Profile**
   - URL: `/api/v1/auth/profile/`
   - Method: GET
   - Headers: `Authorization: Bearer <access_token>`
   - Response: JSON
   ```json
   {
       "id": 1,
       "username": "newuser",
       "email": "user@example.com"
   }
   ```

5. **Token Refresh**
   - URL: `/api/v1/auth/token/refresh/`
   - Method: POST
   - Request Body:
   ```json
   {
       "refresh": "refresh_token_here"
   }
   ```
   - Response: JSON
   ```json
   {
       "access": "new_access_token_here"
   }
   ```

### Chat API
1. **List Chat Sessions**
   - URL: `/api/v1/chat/sessions/`
   - Method: GET
   - Headers: `Authorization: Bearer <access_token>`
   - Response: JSON
   ```json
   {
       "count": 1,
       "next": null,
       "previous": null,
       "results": [
           {
               "id": "uuid",
               "title": "Chat Session",
               "created_at": "2024-03-13T10:00:00Z",
               "chats": [],
               "last_message": null
           }
       ]
   }
   ```

2. **Create Chat Session**
   - URL: `/api/v1/chat/sessions/`
   - Method: POST
   - Headers: `Authorization: Bearer <access_token>`
   - Request Body:
   ```json
   {
       "title": "New Chat Session"
   }
   ```
   - Response: JSON
   ```json
   {
       "id": "uuid",
       "title": "New Chat Session",
       "created_at": "2024-03-13T10:00:00Z",
       "chats": [],
       "last_message": null
   }
   ```

3. **Get Specific Session**
   - URL: `/api/v1/chat/sessions/<id>/`
   - Method: GET
   - Headers: `Authorization: Bearer <access_token>`
   - Response: JSON
   ```json
   {
       "id": "uuid",
       "title": "Chat Session",
       "created_at": "2024-03-13T10:00:00Z",
       "chats": [],
       "last_message": null
   }
   ```

4. **List Chats in Session**
   - URL: `/api/v1/chat/sessions/<id>/chats/`
   - Method: GET
   - Headers: `Authorization: Bearer <access_token>`
   - Response: JSON
   ```json
   {
       "count": 1,
       "next": null,
       "previous": null,
       "results": [
           {
               "id": 1,
               "message": "Hello",
               "response": "Hi there!",
               "created_at": "2024-03-13T10:00:00Z"
           }
       ]
   }
   ```

5. **Create Chat in Session**
   - URL: `/api/v1/chat/sessions/<id>/chats/`
   - Method: POST
   - Headers: `Authorization: Bearer <access_token>`
   - Request Body:
   ```json
   {
       "message": "Hello, how are you?"
   }
   ```
   - Response: JSON
   ```json
   {
       "id": 1,
       "message": "Hello, how are you?",
       "response": "I'm doing well, thank you! How can I help you today?",
       "created_at": "2024-03-13T10:00:00Z"
   }
   ```

6. **Get Specific Chat**
   - URL: `/api/v1/chat/sessions/<id>/chats/<id>/`
   - Method: GET
   - Headers: `Authorization: Bearer <access_token>`
   - Response: JSON
   ```json
   {
       "id": 1,
       "message": "Hello",
       "response": "Hi there!",
       "created_at": "2024-03-13T10:00:00Z"
   }
   ```

## Error Responses
All API endpoints may return the following error responses:

1. **Authentication Error (401)**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

2. **Permission Error (403)**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

3. **Not Found Error (404)**
```json
{
    "detail": "Not found."
}
```

4. **Validation Error (400)**
```json
{
    "field_name": [
        "Error message"
    ]
}
``` 