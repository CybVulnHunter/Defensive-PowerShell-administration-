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

