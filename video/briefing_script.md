# NationalBank Reserve — Executive Briefing Script
## Checkpoint 5 | 5-Minute Stakeholder Presentation
**Presenter:** Mustafa Musa Ahmed | **Target length:** 5:00 (±30s)

---

## [0:00–0:30] OPENING (30s)

"Good morning. My name is Mustafa Musa Ahmed, and I led the red team
engagement against NationalBank Reserve's simulated infrastructure.

Over 12 weeks, we tested the bank across five phases: scoping and threat
modelling, infrastructure assessment, web and API assessment, social
engineering with detection evasion, and this final executive report.

The headline: our team achieved full compromise of the lab environment in
under 15 minutes. No zero-days. No advanced tooling. Just public exploits,
default credentials, and one phishing email."

---

## [0:30–1:30] WHAT WE FOUND (60s)

"We identified 22 findings. Five are CRITICAL — these are the ones that
directly led to compromise.

First: a database backup file left in the web root exposed full DB
credentials. CVSS 9.8.

Second: SQL injection and command injection in the web application allowed
us to run arbitrary commands on the server as the web user — effectively
remote code execution.

Third: the API had no authentication check on its admin endpoint. Anyone
could access it. And API SQL injection bypassed login entirely.

Fourth: Broken Object Level Authorization let us read any user's record by
simply changing an ID in the URL.

Fifth: a phishing email from a spoofed internal address was delivered and
clicked, and credentials were captured by our credential-harvesting portal.

On top of those, 12 HIGH severity issues — cross-user data leaks, SSRF that
read internal system files, unrestricted file upload, missing security
headers, and outdated software across the stack."

---

## [1:30–2:30] HOW WE COMPROMISED THE BANK (60s)

"Our attack chain looked like this:

Step 1 — Phishing email from it-support@nationalbank.com. The target clicked.
Credentials captured.

Step 2 — We used API broken authentication to reach the admin panel without
a token.

Step 3 — BOLA let us enumerate every user and their API keys.

Step 4 — Mass assignment let us register a new account with the admin role.

Step 5 — SQL injection and command injection gave us a root shell on the
server.

Step 6 — SSRF read internal files, and the exposed backup file leaked the
database password.

The whole chain ran in under 15 minutes with beginner-level skill. Public
exploit references were all we needed.

We also tested detection evasion: signature-only antivirus was bypassed by
custom byte-level obfuscation. The commercial encoder we tried was actually
detected because of its own signature — proving that signature-only AV is not
enough."

---

## [2:30–3:30] BUSINESS IMPACT (60s)

"If this were production:

- Every customer record could be extracted via SQL injection.
- Any user account could be accessed or taken over.
- The web server could be fully controlled by an attacker.
- Internal files including system configuration could be read remotely.
- Fraudulent transactions and regulatory exposure would be immediate.

For a bank of 5,000 employees under RBI and PCI-DSS obligations, this is
not just an IT incident — it's a compliance and reputation crisis."

---

## [3:30–4:30] WHAT WE RECOMMEND (60s)

"We have given you a 90-day defensive roadmap in three phases.

Days 0 to 7 — Containment:
Rotate every credential. Delete backup files. Block domain spoofing with
DMARC, SPF, and DKIM. Enable WAF rules for injection and SSRF patterns.

Days 8 to 30 — Hardening:
Patch outdated software. Implement parameterized queries. Add authorization
checks to every API endpoint. Deploy an EDR solution instead of signature-only
AV. Enforce HttpOnly cookies and security headers.

Days 31 to 90 — Maturity:
Roll out phishing-resistant MFA to privileged users. Segment the network.
Enable centralized logging with SIEM. Run quarterly phishing simulations and
red team exercises.

Success metrics: Critical vulnerabilities patched within 7 days. High severity
within 30 days. Phishing click rate below 5%. Full MFA coverage on admin
accounts."

---

## [4:30–5:00] CLOSING (30s)

"To summarise: the lab environment was compromised in 15 minutes through a
combination of human, application, and infrastructure weaknesses. The
22 findings are documented in the full report with CVSS scores, MITRE ATT&CK
mapping, and evidence. The 90-day roadmap gives a concrete, prioritised path
to remediation.

Our recommendation is to treat the containment phase as urgent — begin today.
The full report and all evidence are in the repository linked in the
submission.

Thank you. I'm happy to take questions."

---

## TIMING CHECKPOINTS

| Time | Section | Cumulative |
|---|---|---|
| 0:00 | Opening | 0:30 |
| 0:30 | What we found | 1:30 |
| 1:30 | Attack chain | 2:30 |
| 2:30 | Business impact | 3:30 |
| 3:30 | Recommendations | 4:30 |
| 4:30 | Closing | 5:00 |

## DELIVERY TIPS

- Speak clearly, moderate pace, pause at each section boundary.
- Put the risk matrix on screen during section 2.
- Show the 90-day roadmap during section 4.
- End with a confident summary line — don't fade out.
