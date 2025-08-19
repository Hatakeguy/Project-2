import os  # Missing import
from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

# Connect to MySQL
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASS", "YOUR_PASSWORD"),
    database=os.environ.get("DB_NAME", "project2_db")
)
cursor = db.cursor(dictionary=True)

# Sessions dictionary to store active sessions
sessions = {}  # Missing sessions dictionary

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    # Fixed variable names (user → username, pw → password)
    sql = "SELECT id, password FROM users WHERE username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result and result['password'] == password:  # Fixed dictionary access
        token = f"token-{username}"  # Fixed variable name
        sessions[token] = username  # Store session
        return jsonify({"success": True, "token": token})
    return jsonify({"success": False})
    
@app.route("/calc", methods=["POST"])
def calc():
    data = request.json
    token = data.get("token")
    
    # Check if token is valid in our sessions
    if token not in sessions:  # Better session validation
        return jsonify({"error": "Invalid token"})
    
    n1 = data.get("num1")
    n2 = data.get("num2")
    op = data.get("op")
    
    # Convert to numbers
    try:
        n1 = float(n1)
        n2 = float(n2)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid numbers"})
    
    try:
        if op == "add":
            result = n1 + n2
        elif op == "sub":
            result = n1 - n2
        elif op == "mul":
            result = n1 * n2
        elif op == "div":
            if n2 == 0:
                return jsonify({"error": "Division by zero"})
            result = n1 / n2
        else:
            return jsonify({"error": "Invalid operation"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
