# Exercise 05: Linux Process Management

> Monitor, manage, and control processes on Linux.

## Goal

Master process management: `ps`, `top`, `kill`, `nohup`, `bg`, `fg`, `jobs`.

## Instructions

### 1. View Running Processes

```bash
# All processes
ps aux

# Processes by current user
ps -u $(whoami)

# Process tree
ps aux --forest

# Specific process
ps aux | grep python
```

### 2. Interactive Monitoring with top/htop

```bash
top                    # Real-time process viewer
    # Inside top:
    # q    = quit
    # k    = kill a process (enter PID)
    # M    = sort by memory
    # P    = sort by CPU
    # u    = filter by user
```

### 3. Background and Foreground Jobs

```bash
# Run a long-running process in background
sleep 100 &

# Or start it then suspend it
sleep 100
# Press Ctrl+Z to suspend

# View background jobs
jobs

# Bring job to foreground
fg %1

# Send to background again
# Press Ctrl+Z, then:
bg %1

# Run in background with output redirected
nohup long-running-command &
```

### 4. Kill Signals

```bash
# SIGTERM (15) - graceful shutdown
kill 1234

# SIGKILL (9) - force kill
kill -9 1234

# SIGHUP (1) - reload configuration
kill -1 1234

# SIGINT (2) - interrupt (Ctrl+C)
kill -2 1234

# Kill by name
killall python

# Kill process trees
pkill -f "node server.js"
```

### 5. Process Priorities

```bash
# Start with lower priority (nice value: -20 to 19, lower = higher priority)
nice -n 10 ./slow-script.sh

# Change priority of running process
renice -n 5 -p 1234
```

### 6. Persistent Sessions with tmux/screen

```bash
# Start a tmux session
tmux new -s mysession

# Inside tmux:
# Ctrl+b then c = new window
# Ctrl+b then n/p = next/previous window
# Ctrl+b then d = detach

# Re-attach
tmux attach -t mysession

# List sessions
tmux ls
```

## Self-Check

- What's the difference between SIGTERM and SIGKILL?
- How do you send a process to the background?
- What's the difference between `nice` and `renice`?

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `ps aux` | List all processes |
| `top` | Interactive process viewer |
| `kill -9 <pid>` | Force kill process |
| `nohup command &` | Run immune to hangups |
| `jobs` | List background jobs |
| `fg/bg` | Foreground/background control |
| `tmux new -s name` | New persistent session |
