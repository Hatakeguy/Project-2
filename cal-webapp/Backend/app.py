import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

# Get database URL from environment (use the internal URL for better performance)
database_url = os.environ.get('DATABASE_URL', 'postgresql://cal_webapp_db_user:Onw8wxtwde33nnw1XXrKWg1RDX2G4vvS@dpg-d2immg6mcj7s73cj2ii0-a/cal_webapp_db')
url = urlparse(database_url) 

# Establish database connection
db = psycopg2.connect(
    host=url.hostname,
    database=url.path[1:],  # Remove leading slash
    user=url.username,
    password=url.password,
    port=url.port
)

# Create cursor with dictionary results
cursor = db.cursor(cursor_factory=RealDictCursor)

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
    except psycopg2.IntegrityError:
        return jsonify({"success": False, "error": "Username exists"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
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
    data = request.get_json()
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
