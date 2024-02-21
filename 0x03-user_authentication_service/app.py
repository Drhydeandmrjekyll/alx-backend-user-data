from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


# Define route for registering users
@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Call register_user method of your Auth class to register user
        AUTH.register_user(email, password)
    except ValueError:
        # Handle the case where the user cannot be registered
        abort(400)

    return jsonify({"email": email, "message": "User created"}), 200


@app.route('/sessions', methods=['POST'])
def log_in():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Call log_in method of your Auth class to log in user
        session_id = AUTH.log_in(email, password)
    except ValueError:
        # Handle the case where the user cannot be logged in
        abort(401)

    return (jsonify({"session_id": session_id, "message": "User logged in"}),
            200)


# Route for updating password
@app.route('/reset_password', methods=['PUT'])
def update_password():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
