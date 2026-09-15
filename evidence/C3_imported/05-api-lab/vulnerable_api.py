#!/usr/bin/env python3
"""
NationalBank Reserve — Checkpoint 3
Intentionally Vulnerable API (LAB ONLY)
For testing API Security Top 10
"""

from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "supersecret123"  # VULN: hardcoded secret

# Initialize in-memory DB
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT, role TEXT, api_key TEXT)")
    c.execute("INSERT INTO users VALUES (1, 'admin', 'admin123', 'admin', 'KEY-ADMIN-001')")
    c.execute("INSERT INTO users VALUES (2, 'alice', 'alice456', 'user', 'KEY-USER-002')")
    c.execute("INSERT INTO users VALUES (3, 'bob', 'bob789', 'user', 'KEY-USER-003')")
    conn.commit()
    return conn

DB = init_db()

# ============================================================
# VULNERABILITY 1: BOLA (Broken Object Level Authorization)
# ============================================================
@app.route("/api/v1/user/<int:user_id>")
def get_user(user_id):
    # VULN: No authorization check - anyone can access any user
    c = DB.cursor()
    c.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    if user:
        return jsonify({"id": user[0], "username": user[1], "role": user[2]})
    return jsonify({"error": "not found"}), 404

# ============================================================
# VULNERABILITY 2: Broken Authentication (No JWT verification)
# ============================================================
@app.route("/api/v1/admin")
def admin_endpoint():
    # VULN: No authentication check
    return jsonify({"message": "Welcome admin", "flag": "FLAG{broken_auth}"})

# ============================================================
# VULNERABILITY 3: Excessive Data Exposure
# ============================================================
@app.route("/api/v1/users")
def list_users():
    # VULN: Returns password and api_key
    c = DB.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    return jsonify([{"id": u[0], "username": u[1], "password": u[2], "role": u[3], "api_key": u[4]} for u in users])

# ============================================================
# VULNERABILITY 4: Mass Assignment
# ============================================================
@app.route("/api/v1/register", methods=["POST"])
def register():
    # VULN: Accepts 'role' from user input
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  # VULN: attacker can set role=admin
    
    c = DB.cursor()
    c.execute("INSERT INTO users (username, password, role, api_key) VALUES (?, ?, ?, ?)",
              (username, password, role, "KEY-NEW-999"))
    DB.commit()
    return jsonify({"message": "registered", "username": username, "role": role})

# ============================================================
# VULNERABILITY 5: Injection (SQLi via login)
# ============================================================
@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "")
    password = data.get("password", "")
    
    # VULN: String concatenation in SQL
    query = f"SELECT id, username, role FROM users WHERE username='{username}' AND password='{password}'"
    try:
        c = DB.cursor()
        c.execute(query)
        user = c.fetchone()
        if user:
            token = jwt.encode({"user": user[1], "role": user[2]}, SECRET_KEY, algorithm="HS256")
            return jsonify({"token": token, "user": user[1]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"error": "invalid credentials"}), 401

# ============================================================
# VULNERABILITY 6: Improper Assets Management - Debug endpoint
# ============================================================
@app.route("/api/v1/debug")
def debug():
    # VULN: Exposes sensitive info
    return jsonify({
        "secret_key": SECRET_KEY,
        "database": "in-memory",
        "users_count": 3,
        "version": "1.0.0"
    })

# ============================================================
# VULNERABILITY 7: Server-Side Request Forgery (SSRF)
# ============================================================
@app.route("/api/v1/fetch")
def fetch_url():
    import urllib.request
    url = request.args.get("url", "")
    # VULN: No URL validation
    try:
        response = urllib.request.urlopen(url, timeout=3)
        return jsonify({"content": response.read(200).decode("utf-8", errors="ignore")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("[*] Starting vulnerable API on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=False)
