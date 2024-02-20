from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


# Route to handle profile
@app.route('/profile', methods=['GET'])
def profile():
    # Get the session ID from the request cookies
    session_id = request.cookies.get('session_id')

    # Find the user with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # If user exists, respond with a 200 HTTP status and user's email
        return jsonify({"email": user.email}), 200
    else:
        # If session ID invalid or user does not exist,respond 403 HTTP status
        return jsonify({"message": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
