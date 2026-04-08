# SSH Honeypot

A lightweight SSH honeypot built with Python and Paramiko. 
Simulates an SSH server on port 22, captures all login attempts 
(IP, username, password), and logs them for threat analysis.

## Features
- Captures attacker IPs, usernames, and passwords
- Multi-threaded — handles multiple attackers simultaneously
- Configurable port via command-line argument
- Log parser with top-10 stats

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/ssh-honeypot
cd ssh-honeypot
pip install -r requirements.txt
ssh-keygen -t rsa -b 2048 -f honeypot_rsa -N ""
python -m honeypot.server --port 2222
```

## Example log output

2026-04-9 03:42:11 CONNECTION | IP: 185.224.128.43
2026-04-9 03:42:12 LOGIN ATTEMPT | IP: 185.224.128.43 | user: root | pass: admin123
2026-04-9 03:42:13 LOGIN ATTEMPT | IP: 185.224.128.43 | user: root | pass: password

## Analyzing logs

```bash
python -m honeypot.log_parser logs/honeypot.log
```

## Legal notice
Only deploy on systems you own. Never run on a network without permission.

## Tech stack
Python · Paramiko · Threading · Sockets

## Demo
![demo](demo.gif)

