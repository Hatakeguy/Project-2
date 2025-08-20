import os
from flask import Flask, request, jsonify
import psycopg2
from urllib.parse import urlparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins


cursor = db.cursor(dictionary=True) db = psycopg2.connect(
    host="dpg-d2immg6mcj7s73cj2ii0-a",  # From your Render DB settings
    database="cal_webapp_db",         # From your Render DB settings
    user="cal_webapp_db_user",                  # From your Render DB settings
    password="Onw8wxtwde33nnw1XXrKWg1RDX2G4vvS",              # From your Render DB settings
    port="5432"                # Probably 5432
)

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

