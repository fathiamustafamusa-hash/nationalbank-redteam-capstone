# NationalBank Reserve — Red Team Engagement
## Checkpoint 5: Executive Pentest Report + Defensive Roadmap

**Analyst:** Mustafa Musa Ahmed | **Year:** 2026  
**Environment:** Authorized lab only (Kali Linux + Docker + Gophish + ffmpeg + espeak-ng)

---

## Executive Summary

Full-scope red team assessment of NationalBank Reserve's simulated banking infrastructure across 5 phases. **Full compromise achieved in under 15 minutes** with no zero-days — just public exploits, default credentials, and one phishing email.

**22 findings:**
- 5 CRITICAL (RCE, auth bypass, DB credential leak)
- 12 HIGH (data theft, privilege escalation, account takeover)
- 3 MEDIUM (defense erosion)
- 2 LOW (info disclosure)

**Overall risk: CRITICAL**

---

## Deliverables

| File | Purpose |
|---|---|
| `report/Checkpoint5_Report.pdf` | Full pentest report (exec summary, risk matrix, 90-day roadmap) |
| `report/Checkpoint5_Report.md` | Markdown source |
| `report/Unified_Findings_Register.pdf` | All 22 findings with CVSS + MITRE ATT&CK |
| `report/Checkpoint4_Report.pdf` | Social engineering + detection evasion report |
| `report/archive/Checkpoint-2-Report.pdf` | Infrastructure assessment |
| `video/briefing_script.md` | 5-minute stakeholder narration script |
| `video/briefing_slides.pdf` | Slide deck |
| `video/NationalBank_Checkpoint5_Briefing_small.mp4` | 5-minute briefing video (7.2 MB) |
| `evidence/` | All raw evidence (C2, C3, C4) |

---

## Attack Chain

1. **Phishing** → credential capture (`it-support@nationalbank.com` spoofed)
2. **API broken auth** → admin panel without token
3. **BOLA** → enumerate all users + API keys
4. **Mass assignment** → self-assign admin role
5. **SQLi + command injection** → root shell on server
6. **SSRF** → internal file read
7. **.bak file** → DB credentials

**Time to compromise: < 15 minutes.**

---

## 90-Day Roadmap (Summary)

- **Days 0–7 (CONTAIN):** Rotate credentials, delete .bak files, enable DMARC/SPF/DKIM, WAF rules
- **Days 8–30 (HARDEN):** Patch software, parameterized queries, API authorization, EDR deployment
- **Days 31–90 (MATURE):** Phishing-resistant MFA, segmentation, SIEM, quarterly red team

---

## MITRE ATT&CK Coverage

T1595, T1592, T1566.002, T1059, T1204.002, T1068, T1027, T1027.002, T1056.003, T1552.001, T1083, T1213, T1565

---

## Safety Notice

All payloads, phishing templates, and techniques are for **authorized lab use only**. Executable payloads and video source files are excluded via `.gitignore`.

---

## Reproducibility

Full commands and evidence chains in each checkpoint report.
