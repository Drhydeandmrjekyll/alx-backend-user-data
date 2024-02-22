from flask import Flask, request, jsonify, Response, make_response, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home() -> Response:
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"])
def register_user() -> Response:
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        message = {"email": email, "message": "user created"}
        return jsonify(message), 200
    except ValueError:
        error_message = {"message": "email already registered"}
        return jsonify(error_message), 400


@app.route("/sessions", methods=["POST"])
def login() -> Response:
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        # Generate session ID
        session_id = AUTH.create_session(email)

        # Create JSON response
        response_data = {"email": email, "message": "logged in"}

        # Create response with JSON data and set session ID cookie
        response = make_response(jsonify(response_data), 200)
        response.set_cookie("session_id", session_id)

        return response
    else:
        # If login is invalid, return 401 Unauthorized
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
