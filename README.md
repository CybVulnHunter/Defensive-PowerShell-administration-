# Defensive-PowerShell-administration
# 🔒 Defensive PowerShell Administration Tool

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-5391FE.svg)](https://docs.microsoft.com/powershell/)

A comprehensive, menu-driven security auditing tool for Windows system administrators. This Python-based interface executes defensive PowerShell commands to assess system security posture, identify misconfigurations, and detect potential security risks.

> ⚠️ **For Authorized System Administration Only**  
> This tool is designed strictly for legitimate security auditing and hardening assessment by authorized personnel.

---

# 📋 Features

## 🔐 Core Security Checks

- **Windows Update Status**  
  - Pending updates  
  - Service health  
  - Installation history  

- **Firewall Configuration**  
  - Profile status  
  - Active rules  
  - Service state  

- **BitLocker Encryption**  
  - Drive encryption status  
  - Encryption methods  
  - Key protectors  

- **Security Policy Compliance**  
  - Password policies  
  - Audit settings  
  - UAC configuration  

---

## 🛡️ Advanced Defensive Audits

- **Windows Defender Status**  
  - Real-time protection  
  - Signature updates  
  - Threat detection  
  - Exclusions  

- **System Hardening Checks**  
  - SMBv1 status  
  - PowerShell execution policies  
  - AppLocker configuration  
  - Credential Guard  

- **User Account Audit**  
  - Local users  
  - Admin group members  
  - Inactive accounts  
  - Password settings  

- **Running Services Audit**  
  - Service inventory  
  - SYSTEM privileges  
  - Unquoted path vulnerabilities  

- **Scheduled Tasks Audit**  
  - Persistence detection  
  - Privilege escalation checks  

- **Network Connections Audit**  
  - Active connections  
  - Listening ports  
  - Process-to-port mapping  

- **Event Log Analysis**  
  - Failed logins  
  - Account modifications  
  - PowerShell execution events  

- **Installed Software Inventory**  
  - Installed programs  
  - Recently added software  
  - Potentially unwanted applications (PUA)  

---

# 📊 Reporting

- Generate a **Full Security Report**
- Export results to: `SecurityAuditReport.txt`
- Consolidated system posture overview

---

# 🚀 Quick Start

## Prerequisites

- Windows 10 / 11 or Windows Server 2016+
- Python 3.6+
- PowerShell 5.1+
- Administrator privileges (recommended)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/defensive-powershell-tool.git
cd defensive-powershell-tool

python security_admin.py

# Right-click PowerShell → Run as Administrator
python security_admin.py


============================================================
DEFENSIVE POWERSHELL ADMINISTRATION TOOL v2.0
Authorized System Administration Only
============================================================

SYSTEM SECURITY & HARDENING CHECKS:
  [1]  Windows Update Status
  [2]  Firewall Configuration
  [3]  BitLocker Encryption Status
  [4]  Local Security Policy Compliance
  [5]  Windows Defender / Antivirus Status
  [6]  System Hardening Configuration

USER & ACCESS AUDITS:
  [7]  Local User Account Audit
  [8]  Running Services Audit
  [9]  Scheduled Tasks Audit

NETWORK & MONITORING:
  [10] Network Connections Audit
  [11] Windows Event Log Analysis

SOFTWARE INVENTORY:
  [12] Installed Software Inventory

REPORTING:
  [13] Generate Full Security Report

SYSTEM:
  [0]  Exit

```
security_admin.py
├── Core Functions
│   ├── run_powershell()
│   └── clear_screen()
├── Security Modules
│   ├── check_windows_update_status()
│   ├── check_firewall_configuration()
│   ├── check_bitlocker_status()
│   ├── check_security_policy()
│   ├── check_windows_defender_status()
│   ├── check_system_hardening()
│   ├── check_local_users()
│   ├── check_running_services()
│   ├── check_scheduled_tasks()
│   ├── check_network_connections()
│   ├── check_event_logs()
│   ├── check_installed_software()
│   └── generate_full_report()
└── Menu Engine
    ├── display_menu()
    ├── get_user_choice()
    └── main()

📧 Disclaimer

This tool is provided strictly for educational and authorized administrative use. Users must ensure they have explicit permission before auditing any system.

The authors assume no liability for misuse.

🔗 Useful References

Microsoft Security Baselines

CIS Windows Benchmarks

PowerShell Security Guidelines

Windows Defender Documentation

