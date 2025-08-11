from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage for users
users = {}

# Helper function to create user response format
def format_user_response(user_id, user_data):
    return {
        'id': user_id,
        'name': user_data['name'],
        'email': user_data['email'],
        'age': user_data.get('age'),
        'created_at': user_data['created_at'],
        'updated_at': user_data['updated_at']
    }

# GET /users - Get all users
@app.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users"""
    user_list = [format_user_response(user_id, user_data) 
                for user_id, user_data in users.items()]
    return jsonify({
        'users': user_list,
        'total': len(user_list)
    }), 200

# GET /users/<id> - Get specific user
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a specific user by ID"""
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(format_user_response(user_id, users[user_id])), 200

# POST /users - Create new user
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    # Check if email already exists
    for user_data in users.values():
        if user_data['email'] == data['email']:
            return jsonify({'error': 'Email already exists'}), 409
    
    # Generate unique ID and create user
    user_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    users[user_id] = {
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age'),
        'created_at': timestamp,
        'updated_at': timestamp
    }
    
    return jsonify(format_user_response(user_id, users[user_id])), 201

# PUT /users/<id> - Update user
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check if email is being updated and already exists
    if 'email' in data and data['email'] != users[user_id]['email']:
        for uid, user_data in users.items():
            if uid != user_id and user_data['email'] == data['email']:
                return jsonify({'error': 'Email already exists'}), 409
    
    # Update user data
    if 'name' in data:
        users[user_id]['name'] = data['name']
    if 'email' in data:
        users[user_id]['email'] = data['email']
    if 'age' in data:
        users[user_id]['age'] = data['age']
    
    users[user_id]['updated_at'] = datetime.now().isoformat()
    
    return jsonify(format_user_response(user_id, users[user_id])), 200

# DELETE /users/<id> - Delete user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    deleted_user = format_user_response(user_id, users[user_id])
    del users[user_id]
    
    return jsonify({
        'message': 'User deleted successfully',
        'deleted_user': deleted_user
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'User Management API is running',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    # Add some sample data for testing
    sample_users = [
        {'name': 'John Doe', 'email': 'john@example.com', 'age': 30},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25},
        {'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35}
    ]
    
    for user_data in sample_users:
        user_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        users[user_id] = {
            **user_data,
            'created_at': timestamp,
            'updated_at': timestamp
        }
    
    print("Flask User Management API")
    print("=" * 30)
    print("Available endpoints:")
    print("GET    /users       - Get all users")
    print("GET    /users/<id>  - Get specific user")
    print("POST   /users       - Create new user")
    print("PUT    /users/<id>  - Update user")
    print("DELETE /users/<id>  - Delete user")
    print("GET    /health      - Health check")
    print("=" * 30)
    
    app.run(debug=True, host='0.0.0.0', port=5000)