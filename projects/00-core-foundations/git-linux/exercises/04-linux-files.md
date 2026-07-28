# Exercise 04: Linux File System & Permissions

> Navigate the file system, manage files, and set permissions.

## Goal

Master Linux file operations: `ls`, `cd`, `cp`, `mv`, `rm`, `chmod`, `chown`, `find`.

## Instructions

### 1. Navigate the File System

```bash
pwd                     # Print working directory
ls                      # List files
ls -la                  # List all files with details
ls -lh                  # Human-readable sizes
cd ~                    # Go home
cd -                    # Go back to previous directory
cd ..                   # Go up one level
```

### 2. Create and Remove Files

```bash
mkdir -p projects/go/src   # Create nested directories
touch test.txt              # Create empty file
cp test.txt backup.txt      # Copy file
mv backup.txt ~/            # Move file
rm test.txt                 # Delete file
rm -rf temp/                # Delete directory and contents
```

### 3. File Permissions

```bash
# Permission format: -rwxr-xr--
# - = file type (d for directory, l for symlink)
# rwx = owner permissions (read, write, execute)
# r-x = group permissions
# r-- = others permissions

echo '#!/bin/bash' > script.sh
echo 'echo "Hello"' >> script.sh

# Make executable
chmod +x script.sh
./script.sh              # Now it runs

# Set specific permissions
chmod 755 script.sh      # rwxr-xr-x
chmod 644 README.md      # rw-r--r--
chmod 600 secret.txt     # rw-------
chmod 400 key.pem        # r--------
```

### 4. Find Files

```bash
# Find by name
find . -name "*.go"

# Find by type
find . -type f -name "*.md"      # Files only
find . -type d -name "test*"     # Directories only

# Find by size
find . -size +1M                  # Files larger than 1MB
find . -size -1k                  # Files smaller than 1KB

# Find by time
find . -mtime -1                  # Modified in last 24 hours
find . -mmin -30                  # Modified in last 30 minutes

# Execute on results
find . -name "*.tmp" -delete     # Delete all .tmp files
find . -name "*.py" -exec wc -l {} \;  # Count lines in .py files
```

### 5. Links

```bash
# Hard link (same inode, same data)
ln original.txt hardlink.txt

# Symbolic link (pointer)
ln -s original.txt symlink.txt

ls -li  # Show inodes and link info
```

### 6. Grep for Text

```bash
# Search in files
grep "TODO" *.go
grep -r "import" .        # Recursive
grep -i "error" *.log     # Case-insensitive
grep -l "main" *.go       # Only filenames
grep -c "func" *.go       # Count matches

# Piped with other commands
history | grep git
ps aux | grep python
```

## Self-Check

- What's the difference between `chmod 755` and `chmod 644`?
- How do you find all `.txt` files modified in the last hour?
- What's the difference between a hard link and a symbolic link?

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `ls -la` | List all files with details |
| `chmod 755 file` | Set precise permissions |
| `find . -name "*.go"` | Find matching files |
| `grep -r "pattern"` | Search recursively |
| `ln -s target link` | Create symbolic link |
