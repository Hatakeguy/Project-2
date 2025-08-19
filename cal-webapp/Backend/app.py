import os
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
sessions = {}

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Basic validation
    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required"})
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return jsonify({"success": True})
    except mysql.connector.errors.IntegrityError:
        return jsonify({"success": False, "error": "Username exists"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
   
    sql = "SELECT id, password FROM users WHERE username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result and result['password'] == password:
        token = f"token-{username}"
        sessions[token] = username
        return jsonify({"success": True, "token": token})
    return jsonify({"success": False, "error": "Invalid credentials"})
    
@app.route("/calc", methods=["POST"])
def calc():
    data = request.json
    token = data.get("token")
    
    # Check if token is valid in our sessions
    if token not in sessions:
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
