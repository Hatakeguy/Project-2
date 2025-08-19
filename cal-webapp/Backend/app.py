from flask import Flask, request, jsonify
from flask_cors import CORS  # ← import CORS

app = Flask(__name__)
CORS(app)  # ← allow all origins

# Hardcoded user for login
users = {"admin": "1234"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if users.get(username) == password:
        return jsonify({"success": True, "token": "dummy-token"})
    else:
        return jsonify({"success": False})
    
@app.route("/calc", methods=["POST"])
def calc():
    data = request.json
    token = data.get("token")
    if token != "dummy-token":
        return jsonify({"error": "Invalid token"})
    n1 = data.get("num1")
    n2 = data.get("num2")
    op = data.get("op")
    try:
        if op == "add":
            result = n1 + n2
        elif op == "sub":
            result = n1 - n2
        elif op == "mul":
            result = n1 * n2
        elif op == "div":
            result = n1 / n2
        else:
            result = "Invalid operation"
    except Exception as e:
        result = str(e)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
