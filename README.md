# Flask REST API Testing Guide

## Setup Instructions

### 1. Create Requirements File

Create a `requirements.txt` file:

```
Flask==2.3.3
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

---

## API Endpoints Testing

### 1. Health Check

**GET /health** - Check if the API is running

```bash
curl -X GET http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "User Management API is running",
  "timestamp": "2024-12-07T10:30:00.123456"
}
```

---

### 2. Get All Users

**GET /users** - Retrieve all users

```bash
curl -X GET http://localhost:5000/users
```

**Expected Response:**
```json
{
  "users": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "John Doe",
      "email": "john@example.com",
      "age": 30,
      "created_at": "2024-12-07T10:00:00.123456",
      "updated_at": "2024-12-07T10:00:00.123456"
    }
  ],
  "total": 3
}
```

---

### 3. Get Specific User

**GET /users/{id}** - Retrieve a specific user

```bash
# Replace {user-id} with an actual user ID from the previous response
curl -X GET http://localhost:5000/users/{user-id}
```

**Expected Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "created_at": "2024-12-07T10:00:00.123456",
  "updated_at": "2024-12-07T10:00:00.123456"
}
```

**Error Response (User not found):**
```json
{
  "error": "User not found"
}
```

---

### 4. Create New User

**POST /users** - Create a new user

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Williams",
    "email": "alice@example.com",
    "age": 28
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Alice Williams",
  "email": "alice@example.com",
  "age": 28,
  "created_at": "2024-12-07T10:30:00.123456",
  "updated_at": "2024-12-07T10:30:00.123456"
}
```

**Create User (Minimum Required Fields):**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mike Brown",
    "email": "mike@example.com"
  }'
```

**Error Response (Missing Required Fields):**
```json
{
  "error": "Name and email are required"
}
```

**Error Response (Email Already Exists):**
```json
{
  "error": "Email already exists"
}
```

---

### 5. Update User

**PUT /users/{id}** - Update an existing user

```bash
# Replace {user-id} with an actual user ID
curl -X PUT http://localhost:5000/users/{user-id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "age": 29
  }'
```

**Expected Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 29,
  "created_at": "2024-12-07T10:30:00.123456",
  "updated_at": "2024-12-07T10:35:00.789012"
}
```

**Update All Fields:**
```bash
curl -X PUT http://localhost:5000/users/{user-id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson-Smith",
    "email": "alice.johnson@example.com",
    "age": 30
  }'
```

---

### 6. Delete User

**DELETE /users/{id}** - Delete a user

```bash
# Replace {user-id} with an actual user ID
curl -X DELETE http://localhost:5000/users/{user-id}
```

**Expected Response (200 OK):**
```json
{
  "message": "User deleted successfully",
  "deleted_user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 29,
    "created_at": "2024-12-07T10:30:00.123456",
    "updated_at": "2024-12-07T10:35:00.789012"
  }
}
```

---

## Testing with Postman

### Import Collection
1. Open Postman
2. Create a new collection called "User Management API"
3. Add the following requests:

#### 1. Health Check
- **Method:** GET
- **URL:** `http://localhost:5000/health`

#### 2. Get All Users
- **Method:** GET
- **URL:** `http://localhost:5000/users`

#### 3. Get User by ID
- **Method:** GET
- **URL:** `http://localhost:5000/users/{{user_id}}`
- **Note:** Create a variable `user_id` in your environment

#### 4. Create User
- **Method:** POST
- **URL:** `http://localhost:5000/users`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "name": "Test User",
  "email": "test@example.com",
  "age": 25
}
```

#### 5. Update User
- **Method:** PUT
- **URL:** `http://localhost:5000/users/{{user_id}}`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "name": "Updated User",
  "age": 26
}
```

#### 6. Delete User
- **Method:** DELETE
- **URL:** `http://localhost:5000/users/{{user_id}}`

---

## Testing Scenarios

### 1. Complete CRUD Flow
```bash
# 1. Create a user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "age": 25}'

# 2. Get the user ID from the response and use it in subsequent requests
# 3. Get all users
curl -X GET http://localhost:5000/users

# 4. Update the user
curl -X PUT http://localhost:5000/users/{user-id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Test User", "age": 26}'

# 5. Get the specific user
curl -X GET http://localhost:5000/users/{user-id}

# 6. Delete the user
curl -X DELETE http://localhost:5000/users/{user-id}

# 7. Try to get the deleted user (should return 404)
curl -X GET http://localhost:5000/users/{user-id}
```

### 2. Error Testing
```bash
# Test invalid endpoint
curl -X GET http://localhost:5000/invalid

# Test creating user with missing data
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete User"}'

# Test updating non-existent user
curl -X PUT http://localhost:5000/users/non-existent-id \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}'

# Test deleting non-existent user
curl -X DELETE http://localhost:5000/users/non-existent-id
```

---

## Key Features Implemented

✅ **GET /users** - Retrieve all users with pagination info  
✅ **GET /users/{id}** - Retrieve specific user by ID  
✅ **POST /users** - Create new user with validation  
✅ **PUT /users/{id}** - Update existing user  
✅ **DELETE /users/{id}** - Delete user  
✅ **Error handling** - Proper HTTP status codes and error messages  
✅ **Data validation** - Required fields and duplicate email checking  
✅ **UUID generation** - Unique IDs for each user  
✅ **Timestamps** - Created and updated timestamps  
✅ **Sample data** - Pre-populated users for testing  

This API provides a solid foundation for understanding REST API development principles and can be extended with features like database integration, authentication, and more complex validation rules.
