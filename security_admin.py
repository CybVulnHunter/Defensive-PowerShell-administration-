#!/usr/bin/env python3
"""
Defensive PowerShell Administration Tool v2.0
Author: System Administrator
Description: Comprehensive menu-driven interface for authorized system
             administration tasks using PowerShell commands for Windows
             security auditing and hardening assessment.
"""

import subprocess
import sys
import os


def clear_screen():
    """Clear the terminal screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def run_powershell(command):
    """
    Execute a PowerShell command and return the output.

    Args:
        command (str): The PowerShell command to execute

    Returns:
        str: The output from the PowerShell command
    """
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            shell=False
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "Command executed successfully (no output)."
        else:
            return f"Error: {result.stderr}"

    except Exception as e:
        return f"Failed to execute command: {str(e)}"


def check_windows_update_status():
    """Check Windows Update status, pending updates, and service status."""
    print("\n" + "=" * 70)
    print("WINDOWS UPDATE STATUS CHECK")
    print("=" * 70)

    print("\n[+] Checking for pending updates...")
    ps_command = r"""
    try {
        $Session = New-Object -ComObject Microsoft.Update.Session
        $Searcher = $Session.CreateUpdateSearcher()
        $HistoryCount = $Searcher.GetTotalHistoryCount()
        $Updates = $Searcher.Search("IsInstalled=0")

        Write-Host "Pending Updates: $($Updates.Updates.Count)"
        if ($Updates.Updates.Count -gt 0) {
            foreach ($Update in $Updates.Updates) {
                Write-Host "  - $($Update.Title)"
            }
        } else {
            Write-Host "  System is up to date."
        }

        if ($HistoryCount -gt 0) {
            $History = $Searcher.QueryHistory(0, 1)
            Write-Host "`nLast Update Installed: $($History[0].Date)"
        }
    } catch {
        Write-Host "Error accessing Windows Update API. Run as Administrator."
    }
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking Windows Update service status...")
    service_cmd = r"Get-Service -Name wuauserv | Select-Object Name, Status, StartType | Format-Table -AutoSize"
    print(run_powershell(service_cmd))

    input("\nPress Enter to return to menu...")


def check_firewall_configuration():
    """Check Windows Firewall configuration and status for all profiles."""
    print("\n" + "=" * 70)
    print("FIREWALL CONFIGURATION CHECK")
    print("=" * 70)

    print("\n[+] Checking Firewall Profiles...")
    ps_command = r"""
    Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction | Format-Table -AutoSize
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking Active Firewall Rules (showing first 15)...")
    rules_cmd = r"""
    Get-NetFirewallRule | Where-Object { $_.Enabled -eq 'True' } | 
    Select-Object DisplayName, Direction, Action, Profile | 
    Format-Table -AutoSize | Select-Object -First 15
    """
    print(run_powershell(rules_cmd))

    print("\n[+] Checking Firewall Service Status...")
    service_cmd = r"Get-Service -Name mpssvc | Select-Object Name, Status, StartType | Format-Table -AutoSize"
    print(run_powershell(service_cmd))

    input("\nPress Enter to return to menu...")


def check_bitlocker_status():
    """Check BitLocker encryption status for all drives."""
    print("\n" + "=" * 70)
    print("BITLOCKER ENCRYPTION STATUS CHECK")
    print("=" * 70)

    print("\n[+] Checking BitLocker availability...")
    check_cmd = r"Get-WindowsOptionalFeature -Online -FeatureName BitLocker | Select-Object FeatureName, State | Format-Table -AutoSize"
    print(run_powershell(check_cmd))

    print("\n[+] Checking Encryption Status for All Volumes...")
    ps_command = r"""
    try {
        $volumes = Get-BitLockerVolume
        if ($volumes) {
            foreach ($vol in $volumes) {
                Write-Host "`nDrive Letter: $($vol.MountPoint)"
                Write-Host "Protection Status: $($vol.ProtectionStatus)"
                Write-Host "Encryption Percentage: $($vol.EncryptionPercentage)%"
                Write-Host "Encryption Method: $($vol.EncryptionMethod)"
                if ($vol.KeyProtector) {
                    Write-Host "Key Protector Types: $($vol.KeyProtector.KeyProtectorType -join ', ')"
                }
                Write-Host ("-" * 40)
            }
        } else {
            Write-Host "No BitLocker volumes found."
        }
    } catch {
        Write-Host "BitLocker module not available or access denied."
        Write-Host "Note: Run as Administrator for complete information."
    }
    """
    print(run_powershell(ps_command))

    print("\n[+] Alternative Check (Manage-BDE)...")
    alt_cmd = r"manage-bde -status"
    print(run_powershell(alt_cmd))

    input("\nPress Enter to return to menu...")


def check_security_policy():
    """Check local security policy compliance and settings."""
    print("\n" + "=" * 70)
    print("LOCAL SECURITY POLICY COMPLIANCE CHECK")
    print("=" * 70)

    print("\n[+] Checking Password Policy...")
    ps_command = r"net accounts"
    output = run_powershell(ps_command)
    if "Minimum password length" in output:
        print(output)
    else:
        print("Unable to retrieve password policy. Run as Administrator.")

    print("\n[+] Checking Security Policy Settings...")
    policy_cmd = r"""
    try {
        $tempFile = "$env:TEMP\secpol.cfg"
        secedit /export /cfg $tempFile /quiet
        Get-Content $tempFile | Select-String -Pattern "PasswordComplexity|MinimumPasswordLength|LockoutBadCount|ClearTextPassword|RequireLogonToChangePassword" | ForEach-Object { $_.Line }
        Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "Unable to export security policy. Run as Administrator."
    }
    """
    print(run_powershell(policy_cmd))

    print("\n[+] Checking Audit Policy (showing key categories)...")
    audit_cmd = r"""
    auditpol /get /category:"Logon/Logoff","Account Management","Object Access","Policy Change" 2>$null | 
    Select-String -Pattern "Success|Failure|No Auditing"
    """
    print(run_powershell(audit_cmd))

    print("\n[+] Checking User Account Control (UAC) Settings...")
    uac_cmd = r"""
    try {
        $uac = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name 'EnableLUA' -ErrorAction SilentlyContinue
        $consentPrompt = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name 'ConsentPromptBehaviorAdmin' -ErrorAction SilentlyContinue
        if ($uac.EnableLUA -eq 1) { 
            Write-Host "UAC Status: ENABLED"
            Write-Host "Admin Consent Prompt Behavior: $($consentPrompt.ConsentPromptBehaviorAdmin)"
        } else { 
            Write-Host "UAC Status: DISABLED (SECURITY RISK!)"
        }
    } catch {
        Write-Host "Unable to check UAC settings."
    }
    """
    print(run_powershell(uac_cmd))

    input("\nPress Enter to return to menu...")


def check_windows_defender_status():
    """Check Windows Defender antivirus status and protection."""
    print("\n" + "=" * 70)
    print("WINDOWS DEFENDER / ANTIVIRUS STATUS CHECK")
    print("=" * 70)

    print("\n[+] Checking Windows Defender Service Status...")
    service_cmd = r"""
    Get-Service -Name WinDefend, SecurityHealthService, wscsvc | 
    Select-Object Name, Status, StartType | Format-Table -AutoSize
    """
    print(run_powershell(service_cmd))

    print("\n[+] Checking Real-Time Protection Status...")
    rt_cmd = r"""
    try {
        $ defenderStatus = Get-MpComputerStatus
        Write-Host "Real-Time Protection: $($defenderStatus.RealTimeProtectionEnabled)"
        Write-Host "Behavior Monitor: $($defenderStatus.BehaviorMonitorEnabled)"
        Write-Host "On-Access Protection: $($defenderStatus.OnAccessProtectionEnabled)"
        Write-Host "Antivirus Signature Last Updated: $($defenderStatus.AntivirusSignatureLastUpdated)"
        Write-Host "Quick Scan Age (Days): $($defenderStatus.QuickScanAge)"
        Write-Host "Full Scan Age (Days): $($defenderStatus.FullScanAge)"
    } catch {
        Write-Host "Unable to retrieve Defender status. May require Administrator privileges."
    }
    """
    print(run_powershell(rt_cmd))

    print("\n[+] Checking for Threat Detections...")
    threat_cmd = r"""
    try {
        $threats = Get-MpThreatDetection
        if ($threats) {
            Write-Host "Recent Threat Detections:"
            $threats | Select-Object -First 5 | Format-Table ThreatID, Resources, InitialDetectionTime, UserRights -AutoSize
        } else {
            Write-Host "No recent threat detections found."
        }
    } catch {
        Write-Host "Unable to retrieve threat history."
    }
    """
    print(run_powershell(threat_cmd))

    print("\n[+] Checking Defender Exclusions (Potential Security Risk)...")
    exclusion_cmd = r"""
    try {
        $prefs = Get-MpPreference
        Write-Host "Path Exclusions: $($prefs.ExclusionPath.Count)"
        if ($prefs.ExclusionPath) { $prefs.ExclusionPath | ForEach-Object { Write-Host "  - $_" } }
        Write-Host "`nExtension Exclusions: $($prefs.ExclusionExtension.Count)"
        if ($prefs.ExclusionExtension) { $prefs.ExclusionExtension | ForEach-Object { Write-Host "  - $_" } }
        Write-Host "`nProcess Exclusions: $($prefs.ExclusionProcess.Count)"
        if ($prefs.ExclusionProcess) { $prefs.ExclusionProcess | ForEach-Object { Write-Host "  - $_" } }
    } catch {
        Write-Host "Unable to retrieve exclusion list."
    }
    """
    print(run_powershell(exclusion_cmd))

    input("\nPress Enter to return to menu...")


def check_running_services():
    """Audit running services and identify potential security risks."""
    print("\n" + "=" * 70)
    print("RUNNING SERVICES AUDIT")
    print("=" * 70)

    print("\n[+] Checking All Running Services...")
    ps_command = r"""
    Get-Service | Where-Object { $_.Status -eq 'Running' } | 
    Select-Object Name, DisplayName, StartType | 
    Sort-Object StartType | Format-Table -AutoSize
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking Services Running as SYSTEM (High Privilege)...")
    system_cmd = r"""
    try {
        Get-WmiObject Win32_Service | Where-Object { $_.State -eq 'Running' -and $_.StartName -eq 'LocalSystem' } | 
        Select-Object Name, DisplayName, StartMode | Format-Table -AutoSize
    } catch {
        Write-Host "Unable to query WMI services."
    }
    """
    print(run_powershell(system_cmd))

    print("\n[+] Checking for Auto-Start Services (Potential Persistence)...")
    auto_cmd = r"""
    Get-Service | Where-Object { $_.StartType -eq 'Automatic' -and $_.Status -eq 'Running' } | 
    Select-Object Name, DisplayName | Format-Table -AutoSize
    """
    print(run_powershell(auto_cmd))

    print("\n[+] Checking for Suspicious Service Paths...")
    path_cmd = r"""
    try {
        Get-WmiObject Win32_Service | Where-Object { $_.PathName -match '.*\.exe.*' } | 
        Select-Object Name, PathName, StartName | 
        Where-Object { $_.PathName -notmatch '^\".*\"' -and $_.PathName -match ' ' } | 
        Format-Table -AutoSize
        Write-Host "`nNote: Services with unquoted paths containing spaces may be vulnerable to hijacking."
    } catch {
        Write-Host "Unable to check service paths."
    }
    """
    print(run_powershell(path_cmd))

    input("\nPress Enter to return to menu...")


def check_local_users():
    """Audit local user accounts and group memberships."""
    print("\n" + "=" * 70)
    print("LOCAL USER ACCOUNT AUDIT")
    print("=" * 70)

    print("\n[+] Listing All Local User Accounts...")
    ps_command = r"""
    Get-LocalUser | Select-Object Name, Enabled, PasswordLastSet, PasswordExpires, LastLogonDate, AccountExpires | Format-Table -AutoSize
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking Local Administrators Group...")
    admin_cmd = r"""
    Get-LocalGroupMember -Group "Administrators" | Select-Object Name, PrincipalSource, ObjectClass | Format-Table -AutoSize
    """
    print(run_powershell(admin_cmd))

    print("\n[+] Checking Remote Desktop Users Group...")
    rdp_cmd = r"""
    try {
        Get-LocalGroupMember -Group "Remote Desktop Users" | Select-Object Name, PrincipalSource | Format-Table -AutoSize
    } catch {
        Write-Host "Remote Desktop Users group is empty or not accessible."
    }
    """
    print(run_powershell(rdp_cmd))

    print("\n[+] Checking for Inactive Accounts (No Login > 90 Days)...")
    inactive_cmd = r"""
    try {
        $90DaysAgo = (Get-Date).AddDays(-90)
        Get-LocalUser | Where-Object { $_.LastLogonDate -lt $90DaysAgo -and $_.Enabled -eq $true } | 
        Select-Object Name, LastLogonDate | Format-Table -AutoSize
    } catch {
        Write-Host "Unable to check inactive accounts."
    }
    """
    print(run_powershell(inactive_cmd))

    print("\n[+] Checking for Accounts with No Password...")
    nopass_cmd = r"""
    try {
        Get-WmiObject Win32_UserAccount -Filter "LocalAccount=True AND Disabled=False" | 
        Where-Object { $_.PasswordRequired -eq $false } | 
        Select-Object Name, PasswordRequired, PasswordChangeable | Format-Table -AutoSize
        Write-Host "`nWARNING: Accounts with no password are a serious security risk!"
    } catch {
        Write-Host "Unable to check password requirements."
    }
    """
    print(run_powershell(nopass_cmd))

    input("\nPress Enter to return to menu...")


def check_network_connections():
    """Audit active network connections and listening ports."""
    print("\n" + "=" * 70)
    print("NETWORK CONNECTIONS AUDIT")
    print("=" * 70)

    print("\n[+] Checking Active TCP Connections...")
    ps_command = r"""
    Get-NetTCPConnection | Where-Object { $_.State -eq 'Established' } | 
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess, State | 
    Format-Table -AutoSize | Select-Object -First 15
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking Listening Ports...")
    listen_cmd = r"""
    Get-NetTCPConnection | Where-Object { $_.State -eq 'Listen' } | 
    Select-Object LocalAddress, LocalPort, OwningProcess | 
    Sort-Object LocalPort | Format-Table -AutoSize | Select-Object -First 15
    """
    print(run_powershell(listen_cmd))

    print("\n[+] Resolving Process Names for Listening Ports...")
    process_cmd = r"""
    try {
        $connections = Get-NetTCPConnection | Where-Object { $_.State -eq 'Listen' } | Select-Object -First 10
        foreach ($conn in $connections) {
            try {
                $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
                Write-Host "$($conn.LocalAddress):$($conn.LocalPort) - $($process.ProcessName) (PID: $($conn.OwningProcess))"
            } catch {
                Write-Host "$($conn.LocalAddress):$($conn.LocalPort) - Unable to resolve PID: $($conn.OwningProcess)"
            }
        }
    } catch {
        Write-Host "Unable to resolve process names."
    }
    """
    print(run_powershell(process_cmd))

    print("\n[+] Checking Network Adapter Configuration...")
    adapter_cmd = r"""
    Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | 
    Select-Object Name, InterfaceDescription, MacAddress, LinkSpeed | Format-Table -AutoSize
    """
    print(run_powershell(adapter_cmd))

    print("\n[+] Checking DNS Servers...")
    dns_cmd = r"""
    Get-DnsClientServerAddress | Where-Object { $_.AddressFamily -eq 2 } | 
    Select-Object InterfaceAlias, ServerAddresses | Format-Table -AutoSize
    """
    print(run_powershell(dns_cmd))

    input("\nPress Enter to return to menu...")


def check_event_logs():
    """Analyze Windows Event Logs for security events."""
    print("\n" + "=" * 70)
    print("WINDOWS EVENT LOG ANALYSIS")
    print("=" * 70)

    print("\n[+] Checking Recent Failed Login Attempts (Last 24 Hours)...")
    ps_command = r"""
    try {
        $StartTime = (Get-Date).AddHours(-24)
        Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625; StartTime=$StartTime} -ErrorAction SilentlyContinue | 
        Select-Object -First 10 | 
        Select-Object TimeCreated, Id, LevelDisplayName, 
        @{Name='Account'; Expression={$_.Properties[5].Value}},
        @{Name='SourceIP'; Expression={$_.Properties[19].Value}} | 
        Format-Table -AutoSize
        $count = (Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625; StartTime=$StartTime} -ErrorAction SilentlyContinue).Count
        Write-Host "`nTotal Failed Logins (24h): $count"
    } catch {
        Write-Host "Unable to retrieve failed login events. Run as Administrator."
    }
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking Successful Logins (Last 24 Hours)...")
    success_cmd = r"""
    try {
        $StartTime = (Get-Date).AddHours(-24)
        Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624; StartTime=$StartTime} -ErrorAction SilentlyContinue | 
        Where-Object { $_.Properties[8].Value -eq 2 -or $_.Properties[8].Value -eq 10 } | 
        Select-Object -First 5 |
        Select-Object TimeCreated,
        @{Name='Account'; Expression={$_.Properties[5].Value}},
        @{Name='LogonType'; Expression={$_.Properties[8].Value}} | 
        Format-Table -AutoSize
    } catch {
        Write-Host "Unable to retrieve successful login events."
    }
    """
    print(run_powershell(success_cmd))

    print("\n[+] Checking Account Management Events...")
    account_cmd = r"""
    try {
        $StartTime = (Get-Date).AddDays(-7)
        Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4720,4726,4732,4738; StartTime=$StartTime} -ErrorAction SilentlyContinue | 
        Select-Object -First 10 | 
        Select-Object TimeCreated, Id, 
        @{Name='Event'; Expression={switch ($_.Id) { 4720 {'User Created'} 4726 {'User Deleted'} 4732 {'Added to Group'} 4738 {'User Changed'} }}},
        @{Name='Target'; Expression={$_.Properties[0].Value}} | 
        Format-Table -AutoSize
    } catch {
        Write-Host "Unable to retrieve account management events."
    }
    """
    print(run_powershell(account_cmd))

    print("\n[+] Checking PowerShell Execution Events...")
    ps_exec_cmd = r"""
    try {
        $StartTime = (Get-Date).AddDays(-1)
        Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; ID=4104; StartTime=$StartTime} -ErrorAction SilentlyContinue | 
        Select-Object -First 5 | 
        Select-Object TimeCreated, LevelDisplayName,
        @{Name='ScriptBlock'; Expression={$_.Message.Substring(0, [Math]::Min(100, $_.Message.Length)) + '...'}} | 
        Format-Table -AutoSize
    } catch {
        Write-Host "Unable to retrieve PowerShell execution events."
    }
    """
    print(run_powershell(ps_exec_cmd))

    input("\nPress Enter to return to menu...")


def check_scheduled_tasks():
    """Audit scheduled tasks for persistence mechanisms."""
    print("\n" + "=" * 70)
    print("SCHEDULED TASKS AUDIT")
    print("=" * 70)

    print("\n[+] Checking All Scheduled Tasks...")
    ps_command = r"""
    Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' } | 
    Select-Object TaskName, TaskPath, Author, State | 
    Format-Table -AutoSize | Select-Object -First 20
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking Tasks Running with SYSTEM Privileges...")
    system_cmd = r"""
    try {
        Get-ScheduledTask | Where-Object { $_.Principal.UserId -eq 'SYSTEM' -and $_.State -ne 'Disabled' } | 
        Select-Object TaskName, TaskPath, Author | Format-Table -AutoSize
    } catch {
        Write-Host "Unable to query task principals."
    }
    """
    print(run_powershell(system_cmd))

    print("\n[+] Checking Tasks with Highest Privileges...")
    highest_cmd = r"""
    try {
        Get-ScheduledTask | Where-Object { $_.Principal.RunLevel -eq 'Highest' -and $_.State -ne 'Disabled' } | 
        Select-Object TaskName, Author | Format-Table -AutoSize
    } catch {
        Write-Host "Unable to check run levels."
    }
    """
    print(run_powershell(highest_cmd))

    print("\n[+] Checking Recently Created Tasks (Last 7 Days)...")
    recent_cmd = r"""
    try {
        Get-ScheduledTask | Where-Object { $_.Date -gt (Get-Date).AddDays(-7) } | 
        Select-Object TaskName, Date, Author | Format-Table -AutoSize
    } catch {
        Write-Host "Unable to check recent tasks."
    }
    """
    print(run_powershell(recent_cmd))

    print("\n[+] Checking Tasks with Actions (Command Executions)...")
    action_cmd = r"""
    try {
        $tasks = Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' } | Select-Object -First 10
        foreach ($task in $tasks) {
            $actions = $task.Actions | Where-Object { $_.Execute }
            if ($actions) {
                Write-Host "`nTask: $($task.TaskName)"
                foreach ($action in $actions) {
                    Write-Host "  Execute: $($action.Execute) $($action.Arguments)"
                }
            }
        }
    } catch {
        Write-Host "Unable to retrieve task actions."
    }
    """
    print(run_powershell(action_cmd))

    input("\nPress Enter to return to menu...")


def check_installed_software():
    """Inventory installed software and check for unauthorized programs."""
    print("\n" + "=" * 70)
    print("INSTALLED SOFTWARE INVENTORY")
    print("=" * 70)

    print("\n[+] Checking Installed Programs (Control Panel)...")
    ps_command = r"""
    Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | 
    Where-Object { $_.DisplayName -ne $null } | 
    Sort-Object DisplayName | Format-Table -AutoSize
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking 64-bit Installed Programs...")
    prog64_cmd = r"""
    Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
    Select-Object DisplayName, DisplayVersion, Publisher | 
    Where-Object { $_.DisplayName -ne $null } | 
    Sort-Object DisplayName | Format-Table -AutoSize
    """
    print(run_powershell(prog64_cmd))

    print("\n[+] Checking for Potentially Unwanted Software...")
    unwanted_cmd = r"""
    $unwanted = @('*torrent*', '*miner*', '*keygen*', '*crack*', '*hack*', '*activator*')
    $installed = Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*, HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Where-Object { $_.DisplayName -ne $null }
    $found = $installed | Where-Object { 
        $name = $_.DisplayName.ToLower()
        foreach ($pattern in $unwanted) {
            if ($name -like $pattern) { return $true }
        }
        return $false
    }
    if ($found) {
        Write-Host "WARNING: Potentially unwanted software detected:"
        $found | Select-Object DisplayName, Publisher | Format-Table -AutoSize
    } else {
        Write-Host "No obvious unwanted software patterns detected."
    }
    """
    print(run_powershell(unwanted_cmd))

    print("\n[+] Checking Recently Installed Software (Last 30 Days)...")
    recent_cmd = r"""
    try {
        $30DaysAgo = (Get-Date).AddDays(-30).ToString('yyyyMMdd')
        Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*, HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
        Where-Object { $_.InstallDate -gt $30DaysAgo -and $_.DisplayName -ne $null } | 
        Select-Object DisplayName, InstallDate, Publisher | Format-Table -AutoSize
    } catch {
        Write-Host "Unable to check recent installations."
    }
    """
    print(run_powershell(recent_cmd))

    input("\nPress Enter to return to menu...")


def check_system_hardening():
    """Check system hardening configuration and compliance."""
    print("\n" + "=" * 70)
    print("SYSTEM HARDENING STATUS CHECK")
    print("=" * 70)

    print("\n[+] Checking SMBv1 Protocol Status (Should be Disabled)...")
    ps_command = r"""
    try {
        $smb1 = Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
        Write-Host "SMBv1 Protocol: $($smb1.State)"
        if ($smb1.State -eq 'Enabled') {
            Write-Host "WARNING: SMBv1 is enabled - major security risk!"
        }
    } catch {
        Write-Host "Unable to check SMBv1 status."
    }
    """
    print(run_powershell(ps_command))

    print("\n[+] Checking PowerShell Execution Policy...")
    exec_cmd = r"""
    Get-ExecutionPolicy -List | Format-Table -AutoSize
    """
    print(run_powershell(exec_cmd))

    print("\n[+] Checking PowerShell Language Mode...")
    lang_cmd = r"""
    $ExecutionContext.SessionState.LanguageMode
    """
    output = run_powershell(lang_cmd).strip()
    print(f"Current Language Mode: {output}")
    if "FullLanguage" in output:
        print("Note: FullLanguage allows all PowerShell functionality.")

    print("\n[+] Checking Windows Script Host Status...")
    wsh_cmd = r"""
    try {
        $wsh = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows Script Host\Settings' -Name 'Enabled' -ErrorAction SilentlyContinue
        if ($wsh.Enabled -eq 0) {
            Write-Host "Windows Script Host: DISABLED (Good for security)"
        } else {
            Write-Host "Windows Script Host: ENABLED"
        }
    } catch {
        Write-Host "Windows Script Host: ENABLED (default)"
    }
    """
    print(run_powershell(wsh_cmd))

    print("\n[+] Checking AppLocker Policy Status...")
    applocker_cmd = r"""
    try {
        $appLocker = Get-AppLockerPolicy -Effective -ErrorAction SilentlyContinue
        if ($appLocker) {
            Write-Host "AppLocker Policy: Configured"
            Write-Host "Rule Collections: $($appLocker.RuleCollections.Count)"
        } else {
            Write-Host "AppLocker Policy: Not Configured"
        }
    } catch {
        Write-Host "AppLocker not available on this system."
    }
    """
    print(run_powershell(applocker_cmd))

    print("\n[+] Checking Credential Guard Status...")
    cred_cmd = r"""
    try {
        $credGuard = Get-WmiObject -Class Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard
        Write-Host "Credential Guard Running: $($credGuard.SecurityServicesRunning)"
        Write-Host "Credential Guard Configured: $($credGuard.SecurityServicesConfigured)"
    } catch {
        Write-Host "Unable to check Credential Guard status."
    }
    """
    print(run_powershell(cred_cmd))

    input("\nPress Enter to return to menu...")


def generate_full_report():
    """Generate a comprehensive security report."""
    print("\n" + "=" * 70)
    print("GENERATING COMPREHENSIVE SECURITY REPORT")
    print("=" * 70)

    report_file = r"C:\Windows\Temp\SecurityAuditReport.txt"

    print(f"\n[+] Generating report at: {report_file}")
    print("[+] This may take a moment...")

    ps_command = rf"""
    $report = @()
    $report += "SECURITY AUDIT REPORT - $(Get-Date)"
    $report += "="*60
    $report += ""

    # System Info
    $report += "SYSTEM INFORMATION:"
    $report += (Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, TotalPhysicalMemory | Format-List | Out-String)
    $report += ""

    # Quick Security Checks
    $report += "SECURITY SUMMARY:"
    try {{
        $defender = Get-MpComputerStatus
        $report += "Defender Real-Time Protection: $($defender.RealTimeProtectionEnabled)"
    }} catch {{ $report += "Defender Status: Unknown" }}

    try {{
        $fw = Get-NetFirewallProfile | Where-Object {{ $_.Enabled -eq $false }}
        if ($fw) {{ $report += "WARNING: Firewall profiles disabled: $($fw.Name -join ', ')" }} 
        else {{ $report += "Firewall: All profiles enabled" }}
    }} catch {{ $report += "Firewall: Unable to check" }}

    try {{
        $updates = (New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0").Updates.Count
        $report += "Pending Updates: $updates"
    }} catch {{ $report += "Pending Updates: Unable to check" }}

    $report += ""
    $report += "LOCAL ADMINISTRATORS:"
    $report += (Get-LocalGroupMember -Group "Administrators" | Out-String)

    $report | Out-File -FilePath "{report_file}" -Encoding UTF8
    Write-Host "Report saved successfully."
    """

    result = run_powershell(ps_command)
    print(result)

    print(f"\n[+] Report generation complete!")
    print(f"[+] Location: {report_file}")
    print("[+] Note: Open the file with Notepad to view full details.")

    input("\nPress Enter to return to menu...")


def display_menu():
    """Display the main menu options."""
    clear_screen()
    print("=" * 70)
    print("DEFENSIVE POWERSHELL ADMINISTRATION TOOL v2.0")
    print("Authorized System Administration Only")
    print("=" * 70)
    print()
    print("SYSTEM SECURITY & HARDENING CHECKS:")
    print("  [1]  Windows Update Status")
    print("  [2]  Firewall Configuration")
    print("  [3]  BitLocker Encryption Status")
    print("  [4]  Local Security Policy Compliance")
    print("  [5]  Windows Defender / Antivirus Status")
    print("  [6]  System Hardening Configuration")
    print()
    print("USER & ACCESS AUDITS:")
    print("  [7]  Local User Account Audit")
    print("  [8]  Running Services Audit")
    print("  [9]  Scheduled Tasks Audit")
    print()
    print("NETWORK & MONITORING:")
    print("  [10] Network Connections Audit")
    print("  [11] Windows Event Log Analysis")
    print()
    print("SOFTWARE INVENTORY:")
    print("  [12] Installed Software Inventory")
    print()
    print("REPORTING:")
    print("  [13] Generate Full Security Report")
    print()
    print("SYSTEM:")
    print("  [0]  Exit")
    print()
    print("=" * 70)


def get_user_choice():
    """Get and validate user menu selection."""
    while True:
        choice = input("Enter your choice [0-13]: ").strip()
        if choice in [str(i) for i in range(0, 14)]:
            return choice
        print("Invalid choice. Please enter a number between 0 and 13.")


def main():
    """Main program loop."""
    if os.name != 'nt':
        print("WARNING: This tool is designed for Windows systems.")
        print("Some features may not work correctly on this platform.")
        input("Press Enter to continue anyway...")

    while True:
        display_menu()
        choice = get_user_choice()

        menu_actions = {
            '1': check_windows_update_status,
            '2': check_firewall_configuration,
            '3': check_bitlocker_status,
            '4': check_security_policy,
            '5': check_windows_defender_status,
            '6': check_system_hardening,
            '7': check_local_users,
            '8': check_running_services,
            '9': check_scheduled_tasks,
            '10': check_network_connections,
            '11': check_event_logs,
            '12': check_installed_software,
            '13': generate_full_report,
            '0': lambda: sys.exit("\nExiting Defensive PowerShell Administration Tool.\nStay secure!")
        }

        action = menu_actions.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)