# ITSC-200 - Secure Networking Fundamentals Labs
**Brandon Stewart**

---

## Overview

This section covers the labs I completed during ITSC-200: Secure Networking Fundamentals. It was one of the first courses where I got real hands-on time with the tools and concepts that sit at the core of network security - things like firewall configuration, traffic analysis, and active reconnaissance. Each lab builds on the last, starting from the basics of virtual machine networking and working up to deploying and attacking live services in a controlled environment. The write-ups below reflect what I built, what I found, and what I took away from each one.

---

---

## Assignment 1 - Network Topology & Asset Management

**Topic:** Network Mapping | Asset Inventory | Nmap Reconnaissance

### What I Did
Built and documented a full network topology of a lab environment, identified all assets on the subnet, and performed a comprehensive suite of **Nmap scans** to enumerate hosts, open ports, services, and OS details(None of these machinese are in use anymore and the associated IPs/MACs are no longer relevant).

### Network Asset Inventory

| Asset | IP | MAC | Hostname | OS | Open Port | Service |
|---|---|---|---|---|---|---|
| DNS | 10.222.111.65 / .70 | 08:00:27:16:F3:F6 | UbuntoDNS | Ubuntu | 53/tcp | ISC BIND 9.18.30 |
| DHCP | 10.222.111.66 | 08:00:27:69:23:03 | Vbox | Debian | - | - |
| Web | 10.222.111.67 | 08:00:27:62:64:c7 | UbuntuWEB | Ubuntu | 80/tcp | Apache httpd 2.4.58 |
| Client | 10.222.111.72 | 08:00:27:8d:e5:1c | BrandonKali | Kali | - | - |

### Nmap Scans Performed

| Command | Purpose | Key Result |
|---|---|---|
| `nmap 10.222.111.64/27` | Default host discovery | 5 hosts up; DNS on port 53, Web on port 80 |
| `nmap -sS -T4` | SYN stealth scan, aggressive timing | Same results; completed in 40.30s |
| `nmap -sS -T5` | SYN stealth scan, insane timing | Same results; 28.50s - faster but noisier |
| `nmap -sS -D RND:10` | Decoy scan (10 random decoy IPs) | Masks true scan origin; completed in 149.50s |
| `nmap -sS -T2 --scan-delay 500ms` | Slow stealth scan | Took 1056.59s - maximally evasive |
| `nmap -sT` | Full TCP connect scan | Shows `conn-refused` instead of `reset` for closed ports |
| `nmap -sU -T4` | UDP scan | Revealed many open/filtered UDP ports on web server |
| `nmap -sV` | Service version detection | Confirmed ISC BIND 9.18.30 and Apache 2.4.58 |
| `nmap -O` | OS detection | Identified Linux kernel; inconclusive fingerprints on some hosts |
| `nmap -A` | Aggressive scan (OS + version + scripts) | Full service detail including HTTP title, server headers, traceroute |

### Skills Demonstrated
- Subnet scanning and host discovery
- Asset documentation and logical topology mapping
- Multiple Nmap scan types: SYN, TCP connect, UDP, decoy, version, OS, and aggressive
- Understanding of how timing and scan type affect detectability and accuracy

---

## Assignment 2 - Secure Network Build: PFSense Firewall & Multi-Service Infrastructure

**Topic:** Firewall Configuration | Network Segmentation | Service Deployment | Traffic Analysis

### What I Did
Designed and implemented a full secure network environment using **PFSense** as the firewall/router, segmented into LAN and OPT1 subnets. Configured firewall rules, DHCP assignments, gateways, static IPs, and verified connectivity across services using Wireshark.

### Network Architecture
- **PFSense** as the central firewall and gateway for two internal networks (LAN and OPT1)
- **Firewall aliases** created for IP and port groupings (LAN_Server, Server Services)
- **Static IP assignment** for the server on the LAN segment with shared DNS/gateway settings
- DHCP configured and assigned across both LAN and OPT1 interfaces

### Services Deployed & Verified
- **Internet Access** - confirmed outbound connectivity from the Kali client
- **Internal Web Server** - accessed via HTTP; confirmed with Wireshark showing 3-way TCP handshake on port 80
- **SSH Server** - remote shell access verified; 3-way TCP handshake captured on port 22
- **FTP Server** - file transfer access confirmed; 3-way TCP handshake captured on port 21

### Wireshark Traffic Analysis
Each service connection was verified in Wireshark using targeted filters:
- **Google (internet):** TCP handshake on port 443 (HTTPS), filtered to show only client subnet traffic
- **Web Server:** TCP handshake on port 80, filtered between client IP range and server IP
- **SSH:** TCP handshake on port 22, filtered between client and server
- **FTP:** TCP handshake on port 21, filtered between client and server

### Skills Demonstrated
- Firewall rule creation and alias management in PFSense
- Network segmentation across multiple interfaces
- Multi-protocol service deployment (HTTP, SSH, FTP)
- Wireshark filtering and TCP handshake verification

---

## Lab 1 - Virtual Machine Networking & Adapter Configuration

**Topic:** Virtualization Fundamentals | Network Adapter Types

### What I Did
Configured a virtual machine (VM) across three different network adapter modes - **Bridged**, **NAT**, and **Host-Only** - and analyzed the behavior, internet accessibility, and IP addressing of each.

### Key Findings

| Adapter | Internet Access | Unique Characteristic |
|---|---|---|
| **Bridged** | Full | VM appears as its own device on the physical network with its own IP, unmasked from the host |
| **NAT** | Full | VM shares the host's IP address externally - traffic is masked as coming from the host machine |
| **Host-Only** | None | Creates a self-contained private network between the host and VM; no external routing |

### Skills Demonstrated
- Understanding of virtualization networking fundamentals
- Differentiating between NAT, Bridged, and isolated network modes
- Practical IP address analysis and network behavior observation

---

## Lab 2 - Advanced Linux Installation: Gentoo

**Topic:** OS Installation from Source | Linux Internals | Technical Documentation

### What I Did
Worked through the installation of **Gentoo Linux** from scratch using the official Gentoo Handbook as the primary reference. This exercise was meant to give us a hands on experience with bare-meteal OS configuration, including sharing my personal experince with the class. 

### Key Learning Objectives
- Following complex technical documentation step-by-step (Gentoo Handbook for AMD64)
- Hands-on exposure to disk partitioning, formatting, and Linux file systems
- Understanding OS internals at a deeper level than a standard distro install
- VM file sharing between guest and host
- Troubleshooting in a low-guidance environment
- Note-taking and knowledge sharing through a 5-10 minute group presentation

### Skills Demonstrate
- Reading and applying official technical documentation
- Advanced VM management and OS-level configuration
- Linux file system concepts (partitioning, formatting)
- Troubleshooting and in-class knowledge sharing

---

## Lab 3 - Packet Capture & Traffic Analysis with Wireshark

**Topic:** Network Traffic Analysis | Protocol Identification | Anomaly Detection

### What I Did
Analyzed network captures using **Wireshark**, investigating TCP streams, MAC-level traffic statistics, cross-machine communication, and anomalous traffic patterns to identify potential threats.

### Key Findings

**Part 1 - TCP Traffic Analysis:**
- Identified the device sending the most data: MAC address `08:00:27:8d:e5:1c` - transmitted **134 kB** and the highest packet count
- Used TCP stream following to trace individual connections

**Part 2 - Cross-Machine Communication:**
- Observed **mDNS (Multicast DNS)** protocol being used to resolve hostnames to local IP addresses when pinging between machines on the local network

**Part 3 - Anomaly Detection:**
- Identified a hidden message: **"flip-flop"** embedded in the traffic
- Detected suspicious pattern: data arriving from **unique IP addresses** all targeting `192.168.1.75` with **sequential port numbers ranging from 1484-1611** - characteristic of a port scan or coordinated probe
- Identified `192.168.1.75` as the **firewall/gateway** - a high-value target

### Skills Demonstrated
- Wireshark TCP stream analysis and statistics
- MAC address-level traffic attribution
- mDNS protocol identification
- Anomalous traffic pattern recognition (sequential port probing)

---

## Lab 4 - Network Reconnaissance with Nmap

**Topic:** Active Reconnaissance | Port Scanning | Scan Detection

### What I Did
Performed and analyzed **Nmap port scans** using different timing configurations, comparing scan signatures in Wireshark and evaluating detection risk vs. stealth trade-offs.

### Scan Comparison (Wireshark Analysis)
Both scans shared these indicators of a port scan in progress:
- Large variety of **destination ports** hit with SYN requests
- **SYN-ACK** responses for open ports and **RST** responses for closed ports
- Burst of SYN packets over a very short time window

**Timing difference observed:**
- Scan 1 (standard T4): **0.8693 seconds** from first SYN to last ACK
- Scan 2 (modified): **1.242 seconds** - slightly slower, showing the effect of timing modifiers

### Nmap Timing Intervals - Trade-off Analysis

| Timing | Pro | Con |
|---|---|---|
| **T0** (Paranoid) | Maximum stealth; very hard to detect | Extremely slow; impractical for large networks |
| **T3** (Normal) | Balanced speed and stealth | May still trigger intrusion alerts |
| **T5** (Insane) | Fastest; ideal for large networks | Very likely to be detected; may reduce accuracy |

**Stealth recommendation:** `-T1` (Sneaky) - slow enough to evade most detection thresholds while remaining more practical than T0.

### Skills Demonstrated
- Nmap scanning techniques and timing parameter usage
- Wireshark-based scan signature identification
- Understanding of detection risk vs. reconnaissance efficiency
- Practical stealth assessment methodology

---

## Lab 5 - PFSense Firewall Setup & Network Segmentation

**Topic:** Firewall Deployment | Network Segmentation | Inter-VLAN Routing

### What I Did
Installed and configured **PFSense** from scratch in a virtualized environment, connected multiple machines, and segmented the network into isolated subnets using the OPT1 interface.

### Lab Walkthrough

**Part 1 - PFSense Installation:**
- Installed PFSense and verified the environment was functional
- Confirmed Kali machine had internet access on the internal network

**Part 2 - GUI Configuration:**
- Accessed the PFSense web GUI and completed initial setup with default settings

**Part 3 - Multi-Machine Communication:**
- Added a **Debian Metasploitable** machine to the network
- Established communication between machines using **Netcat** (`nc -l -p`) to test raw TCP connectivity

**Part 4 - Network Segmentation:**
- Added a second internal network on the **OPT1** interface
- Enabled OPT1 in the GUI and assigned an IP range
- Configured **DHCP** on OPT1 with a defined address pool
- Set up **DNS** for external access
- Verified IP renewal and confirmed cross-network communication via **Wireshark**

### Skills Demonstrated
- Firewall installation and baseline configuration
- GUI-based network management
- Netcat for network connectivity testing
- DHCP and DNS configuration
- Network segmentation and inter-network traffic capture

---

## Lab 6 - FTP and SSH Service Configuration

**Topic:** Network Services | Encrypted vs. Unencrypted Protocols | Remote Access

### What I Did
Deployed and tested two critical network services - **FTP** (File Transfer Protocol) and **SSH** (Secure Shell) - across machines on the same network segment, and captured the traffic for analysis.

### Services Configured

**Part 1 - FTP with VSFTPD:**
- Installed and configured the **VSFTPD** FTP server on the Debian machine
- Connected from the Kali machine and browsed the remote directory
- Demonstrated unencrypted file transfer capability

**Part 2 - SSH:**
- Installed and configured **SSH** on the Debian machine
- Established a secure remote shell session from Kali to Debian
- Captured the SSH session in Wireshark - demonstrating encrypted traffic vs. the plaintext nature of FTP

### Skills Demonstrated
- FTP server installation and configuration (VSFTPD)
- SSH setup and remote access
- Understanding of plaintext vs. encrypted protocol security implications
- Wireshark capture and analysis of service traffic

---

## Lab 7 - Web Server Deployment & Vulnerability Scanning with ZAP

**Topic:** Web Server Hardening | Directory Enumeration | OWASP ZAP | Firewall Rules

### What I Did
Deployed an **Apache2 web server**, performed directory enumeration using **dirb**, conducted a web vulnerability scan using **OWASP ZAP**, and explored how client-side manipulation differs from server-side activity in Wireshark.

### Lab Walkthrough

**Part 1 - Apache2 Web Server:**
- Installed and confirmed Apache2 was running
- Accessed the web page from an external network via Kali
- Modified the server's `index` file and created an `admin` folder within the HTML directory
- Ran **dirb** to enumerate the web server's directory structure and discover exposed paths

**Part 2 - OWASP ZAP Vulnerability Scanning:**
- Used **ZAP proxy** to inspect and interact with the web server, successfully reading the contents of the admin folder
- Modified the site header to display "has been hacked" - demonstrating client-side HTML manipulation via proxy interception
- Changed a `.png` filename in the site for Wireshark search testing

**Key Observation - Wireshark:**
> Changes made via ZAP (editing HTML in-browser/proxy) did **not** appear in Wireshark captures, because ZAP modifies content *after* it enters the local network. Wireshark captures network-layer traffic - not post-receipt content manipulation.

**Part 3 - Firewall Rules:**
- Reviewed and configured firewall rules for both **LAN** and **OPT1** interfaces to control access to the web server

### Skills Demonstrated
- Apache2 web server installation and configuration
- Directory enumeration with dirb
- Web vulnerability scanning with OWASP ZAP
- Understanding of proxy-based vs. network-level traffic visibility
- Firewall rule management for service access control

---

## Summary of Skills Acquired

| Domain | Tools & Technologies |
|---|---|
| **Virtualization** | VirtualBox (Bridged, NAT, Host-Only adapters), Gentoo Linux installation |
| **Firewall & Routing** | PFSense, firewall rules, aliases, DHCP, DNS, gateways |
| **Traffic Analysis** | Wireshark, TCP stream analysis, packet filtering |
| **Reconnaissance** | Nmap (SYN, TCP, UDP, decoy, version, OS, aggressive scans), dirb (directory enumeration) |
| **Asset Management** | Network topology mapping, asset inventory, subnet scanning |
| **Network Services** | Apache2, VSFTPD (FTP), SSH, Netcat |
| **Web Security** | OWASP ZAP, proxy interception, HTML manipulation |
| **Network Protocols** | TCP/IP, mDNS, HTTP, HTTPS, SSH, FTP, DNS, UDP |
| **Scripting & CLI** | Linux CLI, `nc`, `ip a`, `dirb`, `nmap` |

---

*Portfolio compiled by Brandon Stewart - ITSC-200 Secure Networking*
