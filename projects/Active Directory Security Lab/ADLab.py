#!/usr/bin/env python3
"""
phase2_toolkit.py Phase 2 Secure System Toolkit - HARDENED VERSION

Author: Makya A****, Brandon Stewart

FUZZING REMEDIATIONS APPLIED:
1. Blank name validation
2. Long name length limits
3. Group existence verification
4. PowerShell injection prevention (enhanced)
5. Invalid character filtering for names
6. Password comparison checks
"""

# -----------------------------
# MODULE IMPORTS (Requirement: Modules)
# -----------------------------
import subprocess   # Used to run PowerShell commands from Python
import sys          # Used for clean program exit and error handling
import os           # Used for file path management and verification
import re           # Used for input validation and sanitization
from datetime import datetime  # Used for timestamps in log entries


# -----------------------------
# CONFIGURATION VARIABLES
# -----------------------------
DOMAIN_NAME = "local.host"
DOMAIN_DN = "DC=local,DC=host"
LAB_PASSWORD = "TypePasswordHere"
LOG_FILE = "user_creation_log.txt"

# FUZZING FIX #2: Name length constraints
MAX_NAME_LENGTH = 64
MIN_NAME_LENGTH = 1

# FUZZING FIX #5: Allowed characters for names (letters, spaces, hyphens, apostrophes)
NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z\s'\-]*$")


# ==============================================================
# FUNCTION BLOCK 1: POWER SHELL INVOCATION HELPERS
# ==============================================================

def run_ps(cmd: str):
    """
    Run a PowerShell command using subprocess and return:
    - exit code
    - standard output
    - error output
    """
    full = [
        "powershell.exe", "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-Command", cmd
    ]
    proc = subprocess.run(full, capture_output=True, text=True)
    return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "").strip()


def escape_ps_str(s: str) -> str:
    """
    FUZZING FIX #4: Enhanced PowerShell injection prevention.
    Escape single quotes AND strip dangerous characters.
    """
    if s is None:
        return ""
    # Remove any backticks, semicolons, pipes, and other shell metacharacters
    s = s.replace("`", "").replace(";", "").replace("|", "")
    s = s.replace("$", "").replace("&", "").replace("<", "").replace(">", "")
    return s.replace("'", "''")


# ==============================================================
# FUNCTION BLOCK 2: INPUT VALIDATION (FUZZING REMEDIATIONS)
# ==============================================================

def validate_name(name: str, field_name: str) -> tuple[bool, str]:
    """
    FUZZING FIX #1, #2, #5, #6: Comprehensive name validation.
    
    Checks:
    - Not blank/empty
    - Within length limits
    - Contains only allowed characters
    - Not same as password
    
    Returns: (is_valid, error_message)
    """
    # FUZZING FIX #1: Check for blank names
    if not name or name.strip() == "":
        return False, f"{field_name} cannot be blank or empty."
    
    name = name.strip()
    
    # FUZZING FIX #2: Check length constraints
    if len(name) < MIN_NAME_LENGTH:
        return False, f"{field_name} must be at least {MIN_NAME_LENGTH} character long."
    
    if len(name) > MAX_NAME_LENGTH:
        return False, f"{field_name} cannot exceed {MAX_NAME_LENGTH} characters."
    
    # FUZZING FIX #5: Check for invalid characters
    if not NAME_PATTERN.match(name):
        return False, (f"{field_name} contains invalid characters. "
                      "Only letters, spaces, hyphens, and apostrophes are allowed. "
                      "Must start with a letter.")
    
    # FUZZING FIX #6: Ensure name is not the same as password
    if name.lower() == LAB_PASSWORD.lower():
        return False, f"{field_name} cannot be the same as the system password."
    
    return True, ""


def validate_groups(groups_line: str) -> tuple[bool, str, list]:
    """
    FUZZING FIX #3: Verify that AD groups exist before attempting to add users.
    
    Returns: (all_valid, error_message, valid_groups_list)
    """
    if not groups_line or not groups_line.strip():
        return True, "", []  # No groups specified is valid
    
    groups = [g.strip() for g in groups_line.split(",") if g.strip()]
    valid_groups = []
    invalid_groups = []
    
    for group in groups:
        # Escape group name for PowerShell
        group_escaped = escape_ps_str(group)
        
        # Check if group exists in AD using LDAP filter
        cmd = f"if (Get-ADGroup -LDAPFilter '(name={group_escaped})' -ErrorAction SilentlyContinue) {{ 'EXISTS' }} else {{ 'MISSING' }}"
        rc, out, err = run_ps(cmd)
        
        if out.strip() == "EXISTS":
            valid_groups.append(group)
        else:
            invalid_groups.append(group)
    
    if invalid_groups:
        return False, f"The following groups do not exist in AD: {', '.join(invalid_groups)}", valid_groups
    
    return True, "", valid_groups


# ==============================================================
# FUNCTION BLOCK 3: ENVIRONMENT VALIDATION
# ==============================================================

def ensure_ad_module_available():
    """
    Ensures the PowerShell ActiveDirectory module is loaded.
    """
    rc, out, err = run_ps("Import-Module ActiveDirectory -ErrorAction Stop")
    if rc != 0:
        print("\n[ERROR] ActiveDirectory PowerShell module not found.")
        print("Install RSAT / 'AD module for PowerShell' and try again.")
        print(f"Details: {err or out}")
        sys.exit(1)


# ==============================================================
# FUNCTION BLOCK 4: ACTIVE DIRECTORY USER UTILITIES
# ==============================================================

def ad_user_exists(sam: str) -> bool:
    """
    Check if a given samAccountName already exists in AD.
    """
    sam_esc = escape_ps_str(sam)
    cmd = (
        f'if (Get-ADUser -LDAPFilter "(sAMAccountName={sam_esc})" '
        f'-ErrorAction SilentlyContinue) {{ "FOUND" }} else {{ "MISSING" }}'
    )
    _, out, _ = run_ps(cmd)
    return out.strip() == "FOUND"


def generate_unique_sam(given: str, surname: str) -> str:
    """
    Builds a unique samAccountName using:
    - first initial + surname
    - adds numeric suffix if name exists
    """
    base = (given[:1] + surname).replace(" ", "").replace("'", "").replace("-", "").lower()
    sam = base
    i = 1
    while ad_user_exists(sam):
        i += 1
        sam = f"{base}{int(i)}"
    return sam


def get_users_container_dn() -> str:
    """
    Returns a valid AD path: OU=Users or CN=Users depending on environment.
    """
    ou = f"OU=Users,{DOMAIN_DN}"
    cn = f"CN=Users,{DOMAIN_DN}"
    cmd = (
        f'if (Get-ADOrganizationalUnit -LDAPFilter "(distinguishedName={escape_ps_str(ou)})" '
        f'-ErrorAction SilentlyContinue) {{ "{ou}" }} else {{ "{cn}" }}'
    )
    _, out, _ = run_ps(cmd)
    return out.strip()


# ==============================================================
# FUNCTION BLOCK 5: FILE HANDLING
# ==============================================================

def log_action(action: str):
    """
    Writes log entries to a text file with timestamps.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def read_log():
    """
    Reads the log file if it exists and displays the contents.
    """
    if os.path.exists(LOG_FILE):
        print(f"\n--- Log File: {os.path.abspath(LOG_FILE)} ---")
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("\nNo log file found yet.")


# ==============================================================
# CLASS BLOCK
# ==============================================================

class ADUserManager:
    """
    Encapsulates all AD management features with enhanced validation.
    """

    def __init__(self):
        ensure_ad_module_available()
        print(f"Running script from: {os.path.abspath(__file__)}")

    def create_user(self):
        """
        Collects user input with FUZZING VALIDATIONS applied.
        """
        print("\n=== Create New AD User ===")
        
        # FUZZING FIX #1, #2, #5, #6: Validate first name
        while True:
            given = input("First name: ").strip()
            is_valid, error_msg = validate_name(given, "First name")
            if is_valid:
                break
            print(f"[VALIDATION ERROR] {error_msg}")
            log_action(f"Validation failed for first name: {error_msg}")
        
        # FUZZING FIX #1, #2, #5, #6: Validate last name
        while True:
            surname = input("Last name: ").strip()
            is_valid, error_msg = validate_name(surname, "Last name")
            if is_valid:
                break
            print(f"[VALIDATION ERROR] {error_msg}")
            log_action(f"Validation failed for last name: {error_msg}")
        
        department = input("Department (optional): ").strip()
        email_opt = input("Email (blank = auto): ").strip()
        
        # FUZZING FIX #3: Validate groups exist before proceeding
        while True:
            groups = input("Groups (comma separated, optional e.g. GG-Helpdesk,GG-Workstation-Admins): ").strip()
            is_valid, error_msg, valid_groups = validate_groups(groups)
            if is_valid:
                break
            print(f"[VALIDATION ERROR] {error_msg}")
            print("Please re-enter groups or leave blank to skip.")
            log_action(f"Validation failed for groups: {error_msg}")
        
        self.create_ad_user(given, surname, department, email_opt, groups)

    def create_ad_user(self, given: str, surname: str, department: str, email_opt: str, groups_line: str) -> bool:
        """
        Core AD user creation workflow with all validations applied.
        """
        # Build unique identifiers
        sam = generate_unique_sam(given, surname)
        upn = f"{sam}@{DOMAIN_NAME}"
        email = upn if not email_opt else email_opt.strip()
        display = f"{given} {surname}"
        target_path = get_users_container_dn()

        # Display summary
        print("\n--- User Creation Summary ---")
        print(f"Display Name    : {display}")
        print(f"samAccountName  : {sam}")
        print(f"UPN             : {upn}")
        print(f"Email           : {email}")
        print(f"Department      : {department}")
        print(f"Container       : {target_path}")
        print(f"Groups          : {groups_line}")
        print(f"Temporary Pass  : {LAB_PASSWORD}")

        resp = input("\nProceed with user creation? (Y/N): ").strip().lower()
        if resp != "y":
            print("User creation cancelled.")
            log_action(f"User creation cancelled for {display}")
            input("Press Enter to return to menu...")
            return False

        # Escape strings for PowerShell (with enhanced sanitization)
        display_e = escape_ps_str(display)
        given_e = escape_ps_str(given)
        surname_e = escape_ps_str(surname)
        sam_e = escape_ps_str(sam)
        upn_e = escape_ps_str(upn)
        email_e = escape_ps_str(email)
        dept_e = escape_ps_str(department or "")
        path_e = escape_ps_str(target_path)
        pw_e = escape_ps_str(LAB_PASSWORD)

        # Build PowerShell command for New-ADUser
        ps_new_user = (
            "New-ADUser "
            f"-Name '{display_e}' "
            f"-GivenName '{given_e}' -Surname '{surname_e}' "
            f"-DisplayName '{display_e}' "
            f"-SamAccountName '{sam_e}' -UserPrincipalName '{upn_e}' "
            f"-EmailAddress '{email_e}' -Department '{dept_e}' "
            f"-Path '{path_e}' "
            f"-AccountPassword (ConvertTo-SecureString '{pw_e}' -AsPlainText -Force) "
            "-Enabled $true -ChangePasswordAtLogon $true -ErrorAction Stop"
        )

        # Execute user creation
        rc, out, err = run_ps(ps_new_user)
        if rc != 0:
            print("\n[ERROR] User creation failed:")
            print(err or out)
            log_action(f"FAILED to create user {sam}: {err or out}")
            input("Press Enter to return to menu...")
            return False

        # FUZZING FIX #3: Only add to validated groups
        groups_added = []
        if groups_line and groups_line.strip():
            # Re-validate groups just before adding (safety check)
            is_valid, error_msg, valid_groups = validate_groups(groups_line)
            
            if is_valid:
                for g in valid_groups:
                    g_e = escape_ps_str(g)
                    ps_add = f"Add-ADGroupMember -Identity '{g_e}' -Members '{sam_e}' -ErrorAction Stop"
                    rc2, out2, err2 = run_ps(ps_add)
                    if rc2 == 0:
                        groups_added.append(g)
                    else:
                        print(f"[WARN] Failed to add '{sam}' to group '{g}': {err2 or out2}")
                        log_action(f"WARN: Failed to add {sam} to group {g}")
            else:
                print(f"[WARN] Group validation failed during add: {error_msg}")

        # Retrieve DN for confirmation
        ps_get_dn = (
            f"$u = Get-ADUser -Identity '{sam_e}'; "
            "if ($u) { $u.DistinguishedName } else { '' }"
        )
        _, dn_out, _ = run_ps(ps_get_dn)
        dn = dn_out.strip()

        # Final summary
        print("\n=== User Created Successfully ===")
        print(f"SamAccountName : {sam}")
        print(f"UPN            : {upn}")
        print(f"DN             : {dn}")
        print(f"TempPassword   : {LAB_PASSWORD}")
        print(f"GroupsAdded    : {', '.join(groups_added)}")

        log_action(f"SUCCESS: Created user {sam} ({display}) in {target_path} Groups: {groups_added}")
        input("\nPress Enter to return to menu...")
        return True

    def apply_rule_template(self):
        """
        Stub for Phase 3: simulate applying role-based access rules.
        """
        user = input("Enter samAccountName to target: ").strip()
        rule = input("Enter rule name (e.g., 'Helpdesk-Min'): ").strip()
        print(f"Pretending to apply rule '{rule}' to user '{user}'...")
        log_action(f"Rule '{rule}' applied to user '{user}' (stub action).")
        input("\nPress Enter to return to menu...")


# ==============================================================
# MAIN MENU FUNCTION 
# ==============================================================

def main_menu():
    """
    Provides a simple menu interface for the toolkit.
    """
    manager = ADUserManager()
    while True:
        print("\n===== Phase 2 Toolkit - HARDENED =====")
        print("1) Create new user")
        print("2) Apply rule template (stub)")
        print("3) View log file")
        print("4) Exit")

        choice = input("Select: ").strip()
        choice_num = int(choice) if choice.isdigit() else 0

        if choice_num == 1:
            manager.create_user()
        elif choice_num == 2:
            manager.apply_rule_template()
        elif choice_num == 3:
            read_log()
        elif choice_num == 4:
            print("Exiting.")
            log_action("Script exited normally")
            break
        else:
            print("Invalid choice. Try again.")


# ==============================================================
# PROGRAM ENTRY POINT
# ==============================================================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        log_action("Script interrupted by user")
        sys.exit(0)
