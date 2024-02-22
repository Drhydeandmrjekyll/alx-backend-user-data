from flask import Flask, request, jsonify, Response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
