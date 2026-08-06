"""
W3Schools Python Tutorial - 38: Python File Handling
=====================================================
Topics: Open files, read, write, delete, with statement

Run: python 38-file-handling.py
Reference: https://www.w3schools.com/python/python_file_handling.asp
"""

# ============================================================
# Opening Files
# ============================================================
# The open() function opens a file and returns a file object.
# Modes: 'r' (read), 'w' (write), 'a' (append), 'x' (create)

# Example 1: Different file modes
print("--- File Modes ---")
print("'r'  - Read (default)")
print("'w'  - Write (overwrites existing)")
print("'a'  - Append (adds to end)")
print("'x'  - Create (fails if exists)")
print("'t'  - Text mode (default)")
print("'b'  - Binary mode")
print("'+'  - Read and write")

# ============================================================
# Writing Files
# ============================================================
# Example 2: Writing to a file
print("\n--- Writing Files ---")

# Write mode - creates or overwrites
with open("example.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("This is line 2.\n")
    f.write("This is line 3.\n")

print("Written to example.txt")

# Append mode - adds to end
with open("example.txt", "a") as f:
    f.write("This line was appended.\n")

print("Appended to example.txt")

# Write multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("example.txt", "a") as f:
    f.writelines(lines)

print("Wrote multiple lines")

# ============================================================
# Reading Files
# ============================================================
# Example 3: Reading from a file
print("\n--- Reading Files ---")

# Read entire file
with open("example.txt", "r") as f:
    content = f.read()
    print(f"Full content:\n{content}")

# Read line by line
print("--- Line by Line ---")
with open("example.txt", "r") as f:
    for line_num, line in enumerate(f, 1):
        print(f"{line_num}: {line.rstrip()}")

# Read into a list
with open("example.txt", "r") as f:
    lines = f.readlines()
    print(f"\nAs list ({len(lines)} lines): {lines}")

# Read single line
with open("example.txt", "r") as f:
    first_line = f.readline()
    print(f"First line: {first_line.rstrip()}")

# ============================================================
# The with Statement
# ============================================================
# Example 4: Why use 'with'?
print("\n--- with Statement ---")

# WITHOUT with (manual close)
# file = open("example.txt", "r")
# try:
#     content = file.read()
# finally:
#     file.close()  # Must remember to close!

# WITH with (automatic close)
with open("example.txt", "r") as f:
    content = f.read()
    print(f"Read {len(content)} characters")
    # File automatically closed when exiting 'with' block

print("File automatically closed!")

# ============================================================
# Working with Paths
# ============================================================
# Example 5: File path handling
print("\n--- File Paths ---")

import os
from pathlib import Path

# Get current directory
print(f"Current dir: {os.getcwd()}")

# List files
print(f"\nFiles in current dir:")
for item in os.listdir("."):
    if item.endswith(".txt") or item.endswith(".py"):
        print(f"  {item}")

# Path object (recommended)
path = Path(".")
print(f"\nPath: {path}")
print(f"Absolute: {path.absolute()}")

# ============================================================
# Checking File Existence
# ============================================================
# Example 6: Check if file exists
print("\n--- File Existence ---")

filename = "example.txt"
if os.path.exists(filename):
    print(f"'{filename}' exists!")
    print(f"  Size: {os.path.getsize(filename)} bytes")
    print(f"  Is file: {os.path.isfile(filename)}")
    print(f"  Is dir: {os.path.isdir(filename)}")
else:
    print(f"'{filename}' does not exist!")

# ============================================================
# File Information
# ============================================================
# Example 7: Get file information
print("\n--- File Information ---")

import time

if os.path.exists("example.txt"):
    stat = os.stat("example.txt")
    print(f"Size: {stat.st_size} bytes")
    print(f"Modified: {time.ctime(stat.st_mtime)}")
    print(f"Accessed: {time.ctime(stat.st_atime)}")

# ============================================================
# Working with CSV-like Data
# ============================================================
# Example 8: Read/write structured data
print("\n--- Structured Data ---")

import csv

# Write CSV
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "London"],
    ["Charlie", 35, "Paris"]
]

with open("people.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("Written to people.csv")

# Read CSV
with open("people.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")

# ============================================================
# Binary Files
# ============================================================
# Example 9: Working with binary files
print("\n--- Binary Files ---")

# Write binary data
data = bytes([72, 101, 108, 108, 111])  # "Hello"
with open("binary.dat", "wb") as f:
    f.write(data)

print(f"Written {len(data)} bytes")

# Read binary data
with open("binary.dat", "rb") as f:
    content = f.read()
    print(f"Read: {content}")
    print(f"As string: {content.decode('utf-8')}")

# ============================================================
# Deleting Files
# ============================================================
# Example 10: Deleting files
print("\n--- Deleting Files ---")

# Create a file to delete
with open("temp.txt", "w") as f:
    f.write("This file will be deleted")

print(f"temp.txt exists: {os.path.exists('temp.txt')}")

# Delete with os.remove()
os.remove("temp.txt")
print(f"After deletion: {os.path.exists('temp.txt')}")

# ============================================================
# Temporary Files
# ============================================================
# Example 11: Working with temporary files
print("\n--- Temporary Files ---")

import tempfile

# Create temporary file
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write("Temporary data")
    temp_name = f.name

print(f"Created: {temp_name}")
print(f"Exists: {os.path.exists(temp_name)}")

# Clean up
os.remove(temp_name)
print(f"After cleanup: {os.path.exists(temp_name)}")

# ============================================================
# Practical Examples
# ============================================================
# Example 12: Real-world file operations
print("\n--- Practical Examples ---")

# Count words in a file
def count_words(filename):
    """Count words in a text file."""
    with open(filename, "r") as f:
        content = f.read()
        words = content.split()
        return len(words)

word_count = count_words("example.txt")
print(f"Word count in example.txt: {word_count}")

# Find and replace in file
def find_replace(filename, find, replace):
    """Find and replace text in a file."""
    with open(filename, "r") as f:
        content = f.read()
    
    new_content = content.replace(find, replace)
    
    with open(filename, "w") as f:
        f.write(new_content)
    
    return content.count(find)

replacements = find_replace("example.txt", "line", "LINE")
print(f"Replaced {replacements} occurrences of 'line' with 'LINE'")

# Merge multiple files
def merge_files(output_file, input_files):
    """Merge multiple files into one."""
    with open(output_file, "w") as outfile:
        for input_file in input_files:
            with open(input_file, "r") as infile:
                outfile.write(infile.read())
                outfile.write("\n")

# ============================================================
# Cleanup
# ============================================================
# Remove created files
for f in ["example.txt", "people.csv", "binary.dat"]:
    if os.path.exists(f):
        os.remove(f)
        print(f"Cleaned up: {f}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. open(file, mode): open a file")
print("2. Modes: 'r' (read), 'w' (write), 'a' (append), 'x' (create)")
print("3. with statement: auto-closes file (RECOMMENDED!)")
print("4. read(): entire file, readline(): one line, readlines(): list")
print("5. write(): write string, writelines(): write list")
print("6. os.remove(): delete file")
print("7. os.path.exists(): check if file exists")
print("8. Always use 'with' to ensure files are closed!")
