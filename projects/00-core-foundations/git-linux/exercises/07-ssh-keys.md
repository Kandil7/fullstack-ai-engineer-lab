# Exercise 07: SSH & Remote Access

> Set up SSH keys, configure access, create tunnels, and sync with rsync.

## Goal

Master SSH key-based authentication, configuration, port forwarding, and file transfer.

## Instructions

### 1. Generate SSH Key Pair

```bash
# Generate ed25519 key pair (most secure, recommended)
ssh-keygen -t ed25519 -C "your@email.com"

# Or RSA fallback
ssh-keygen -t rsa -b 4096 -C "your@email.com"
```

You'll be prompted for:
- Save location (default: `~/.ssh/id_ed25519`)
- Passphrase (strongly recommended)

### 2. Copy Public Key to Remote Server

```bash
# Using ssh-copy-id (recommended)
ssh-copy-id user@server.example.com

# Manual method
cat ~/.ssh/id_ed25519.pub | ssh user@server.example.com "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 3. SSH Configuration

Create `~/.ssh/config`:

```ssh-config
# Default settings
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 5
    IdentityFile ~/.ssh/id_ed25519

# Short alias for personal server
Host myserver
    HostName 192.168.1.100
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# GitHub (use different key for automation)
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github-key
```

Then connect with: `ssh myserver`

### 4. SSH Tunnels (Port Forwarding)

```bash
# Local port forwarding (remote -> local)
# Access a service running on remote port 3000 via localhost:9000
ssh -L 9000:localhost:3000 myserver

# Remote port forwarding (local -> remote)
# Expose local port 8080 on remote's port 9000
ssh -R 9000:localhost:8080 myserver

# Dynamic SOCKS proxy
ssh -D 1080 myserver
# Configure browser to use SOCKS proxy at localhost:1080
```

### 5. SCP and rsync

```bash
# Copy file to remote
scp ./local-file.txt myserver:~/remote-file.txt

# Copy from remote
scp myserver:~/remote-file.txt .

# Copy directory recursively
scp -r ./project/ myserver:~/project/

# rsync - efficient sync (recommended for large transfers)
rsync -avz ./project/ myserver:~/project/
# -a = archive mode, -v = verbose, -z = compress

# rsync with delete (mirror local directory)
rsync -avz --delete ./project/ myserver:~/project/
```

### 6. SSH Security Best Practices

On the remote server, edit `/etc/ssh/sshd_config`:

```ssh-config
# Disable password authentication
PasswordAuthentication no

# Disable root login
PermitRootLogin no

# Use only key-based auth
PubkeyAuthentication yes

# Limit users who can SSH
AllowUsers ubuntu deploy

# Change default port (security through obscurity)
Port 2222

# Always restart after changes:
# sudo systemctl restart sshd
```

## Self-Check

- What's the difference between `ssh-keygen -t ed25519` and `-t rsa`?
- What does `ssh-copy-id` do?
- How do you access a remote database through SSH?

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `ssh-keygen -t ed25519` | Generate key pair |
| `ssh-copy-id user@host` | Copy public key |
| `ssh user@host` | Connect to server |
| `ssh -L 9000:localhost:3000 host` | Local port forwarding |
| `scp local remote:` | Copy files |
| `rsync -avz src/ dest/` | Efficient file sync |
