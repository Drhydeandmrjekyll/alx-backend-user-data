from flask import Flask, jsonify, request, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


# Route to handle logout
@app.route('/sessions', methods=['DELETE'])
def logout():
    # Get the session ID from the request cookies
    session_id = request.cookies.get('session_id')

    # Find the user with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # Destroy the session
        AUTH.destroy_session(user.id)
        # Redirect the user to GET /
        return redirect('/')
    else:
        # If the user does not exist, respond with a 403 HTTP status
        return jsonify({"message": "User not found"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
