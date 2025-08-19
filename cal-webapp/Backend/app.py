from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# -----------------------------
# Simple user database (JSON)
# -----------------------------
users = {"admin": "1234", "deepali": "pass"}

# -----------------------------
# Dummy session token store
# -----------------------------
sessions = {}

# -----------------------------
# Login endpoint
# -----------------------------
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

# -----------------------------
# Calculator endpoint
# -----------------------------
@app.route("/calc", methods=["POST"])
def calc():
    data = request.get_json()
    token = data.get("token")

    if token not in sessions:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        n1 = float(data.get("num1"))
        n2 = float(data.get("num2"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid numbers"}), 400

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
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"result": result})

# -----------------------------
# Main entry
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)


