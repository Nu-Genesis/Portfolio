# Active Directory User Management Toolkit
### Scripting for Tool Construction — Final Project Write-Up

---

## Project Overview

This project was developed collaboratively as the final lab for the Scripting for Tool Construction course. The goal was to build a practical, functional script that combined Python and PowerShell to automate a real-world IT task. The result was a command-line toolkit for managing Active Directory (AD) user accounts — automating the creation of users, assigning them to security groups, and maintaining an audit log of all actions taken.

While the script ultimately revealed important lessons about security vulnerabilities in automation tools, the process of building, testing, and hardening it deepened our understanding of Python scripting, PowerShell integration, and Active Directory administration.

---

## What the Script Does

The toolkit (`phase2_toolkit.py`) provides a menu-driven interface for IT administrators to:

- **Create new AD users** — collects first name, last name, department, email, and group memberships, then provisions the account in Active Directory with a temporary password and forced password change on first login.
- **Generate unique usernames** — automatically builds `samAccountName` values using a first-initial-plus-surname convention, appending a numeric suffix if the name already exists.
- **Assign group memberships** — validates that specified security groups exist in AD before attempting to add the new user to them.
- **Apply role templates** — a stub function designed to simulate role-based access control assignment (planned for a future phase).
- **Maintain an audit log** — every action, successful or failed, is written to a timestamped log file for accountability and review.

---

## Technologies Used

**Python** served as the orchestration layer. The script uses several standard library modules:

- `subprocess` — to invoke PowerShell commands from Python and capture their output
- `re` — for input validation using regular expressions
- `os` — for file path management and log file handling
- `sys` — for controlled program exit on critical errors
- `datetime` — for timestamping log entries

**PowerShell** was used as the Active Directory interface, leveraging cmdlets from the `ActiveDirectory` RSAT module:

- `New-ADUser` — to provision accounts with all required attributes
- `Add-ADGroupMember` — to assign users to security groups
- `Get-ADUser` and `Get-ADGroup` — to verify existing objects before operations
- `Get-ADOrganizationalUnit` — to detect whether a custom OU or the default `CN=Users` container should be targeted

The script bridges these two environments by constructing PowerShell command strings in Python and executing them via `subprocess.run()`, then parsing the return codes and output to determine success or failure.

---

## Security Challenges and Remediation

The original version of the script had several significant security vulnerabilities discovered through fuzzing — a testing technique where unexpected, malformed, or malicious inputs are fed to the program to find failure points. This was a valuable and humbling part of the lab.

The hardened version addresses six specific fuzzing findings:

**1. Blank Input Validation**
The original script would pass empty strings through to PowerShell, causing unpredictable behavior. The fix rejects any blank or whitespace-only name input before it reaches the AD cmdlets.

**2. Name Length Limits**
Extremely long strings could exceed Active Directory field limits or cause buffer-related issues downstream. The fix enforces a minimum of 1 character and a maximum of 64 characters for all name fields.

**3. Group Existence Verification**
Attempting to add a user to a non-existent group would cause the PowerShell command to fail silently or throw an unhandled error. The fix queries AD to confirm each group exists before proceeding, and re-validates groups a second time immediately before the `Add-ADGroupMember` call.

**4. PowerShell Injection Prevention**
The most critical vulnerability — user-supplied input was being interpolated directly into PowerShell command strings. This opened the door to command injection attacks. The fix strips shell metacharacters (backticks, semicolons, pipes, `$`, `&`, `<`, `>`) and properly escapes single quotes before any string is embedded in a PowerShell command.

**5. Invalid Character Filtering**
Names containing characters like `%`, `*`, or LDAP wildcards could interfere with directory queries. The fix uses a regular expression whitelist (`^[a-zA-Z][a-zA-Z\s'\-]*$`) to only permit letters, spaces, hyphens, and apostrophes — rejecting anything else.

**6. Password Comparison Check**
A simple but important safeguard: the script verifies that a user's name does not match the system's temporary password, preventing trivially weak account configurations.

---

## Lessons Learned

This project reinforced several key concepts:

**Never trust user input.** Even in an internal tool designed for IT staff, unvalidated input can cause unexpected failures or — more seriously — security vulnerabilities. The fuzzing phase of the lab made this concrete in a way that reading about it never could.

**Python and PowerShell complement each other well.** Python's readability and standard library made it easy to build the validation logic and application structure, while PowerShell's deep integration with Windows and Active Directory made it the right tool for the actual directory operations. Learning to bridge the two taught us to think carefully about where each language's responsibilities begin and end.

**Logging is not optional.** The audit log built into this script reflects real-world IT practice — every provisioning action should be recorded with a timestamp and outcome. This became especially clear when tracing back which inputs had triggered validation errors during testing.

**Security is iterative.** The "hardened" label in the filename reflects the reality that the first version was not secure. Reaching a more robust version required active adversarial testing, not just writing code that worked under normal conditions.

---

## Potential Improvements

Given more time, several enhancements would make this a stronger tool:

- Replace the hardcoded `LAB_PASSWORD` with a secure prompt or integration with a secrets manager
- Add support for bulk user creation from a CSV file
- Implement actual role-based access control logic in place of the current stub
- Add a delete/disable user workflow to complement account creation
- Encrypt or restrict access to the log file to prevent tampering

---

## Conclusion

What started as a straightforward automation script became a meaningful exercise in secure coding, cross-language integration, and the realities of working with enterprise directory services. The vulnerabilities discovered during fuzzing turned a working script into a genuinely instructive lab — demonstrating that building something functional is only the first step, and that hardening it against real-world misuse is where the deeper learning happens.
