from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Simple user database (JSON file)
users = {"admin": "1234", "deepali": "pass"}

# Dummy token store
sessions = {}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = data.get("username")
    pw = data.get("password")

    if user in users and users[user] == pw:
        token = f"token-{user}"
        sessions[token] = user
        return jsonify({"success": True, "token": token})
    return jsonify({"success": False})

@app.route("/calc", methods=["POST"])
def calc():
    data = request.get_json()
    token = data.get("token")
    if token not in sessions:
        return jsonify({"error": "Unauthorized"}), 403

    n1 = float(data.get("num1"))
    n2 = float(data.get("num2"))
    op = data.get("op")

    result = None
    if op == "add":
        result = n1 + n2
    elif op == "sub":
        result = n1 - n2
    elif op == "mul":
        result = n1 * n2
    elif op == "div":
        result = n1 / n2 if n2 != 0 else "Error (div by 0)"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
