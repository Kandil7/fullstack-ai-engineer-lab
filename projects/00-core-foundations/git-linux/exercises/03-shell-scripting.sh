#!/bin/bash
# Exercise 3: Shell Scripting Practice

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Exercise 1: Backup script
backup_script() {
    log_info "Creating backup script..."
    cat > backup.sh << 'EOF'
#!/bin/bash
# backup.sh - Backup directory with timestamp

set -euo pipefail

SRC_DIR="${1:-.}"
DEST_DIR="${2:-/tmp/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${TIMESTAMP}.tar.gz"

mkdir -p "$DEST_DIR"

log_info "Backing up $SRC_DIR to $DEST_DIR/$BACKUP_NAME"
tar -czf "$DEST_DIR/$BACKUP_NAME" -C "$(dirname "$SRC_DIR")" "$(basename "$SRC_DIR")"

log_info "Backup complete: $DEST_DIR/$BACKUP_NAME"
ls -lh "$DEST_DIR/$BACKUP_NAME"
EOF
    chmod +x backup.sh
    log_info "Created backup.sh"
}

# Exercise 2: Log analyzer
log_analyzer() {
    log_info "Creating log analyzer..."
    cat > analyze_logs.sh << 'EOF'
#!/bin/bash
# analyze_logs.sh - Analyze log files for errors

set -euo pipefail

LOG_FILE="${1:-/var/log/syslog}"
ERROR_PATTERN="${2:-ERROR}"

if [[ ! -f "$LOG_FILE" ]]; then
    log_error "Log file not found: $LOG_FILE"
    exit 1
fi

log_info "Analyzing $LOG_FILE for '$ERROR_PATTERN'..."

# Count errors
error_count=$(grep -c "$ERROR_PATTERN" "$LOG_FILE" || true)
log_info "Found $error_count occurrences of '$ERROR_PATTERN'"

# Show last 10 errors with context
log_info "Last 10 errors:"
grep -B2 -A2 "$ERROR_PATTERN" "$LOG_FILE" | tail -30

# Unique error messages
log_info "Unique error messages:"
grep "$ERROR_PATTERN" "$LOG_FILE" | sed 's/.*ERROR: //' | sort | uniq -c | sort -rn
EOF
    chmod +x analyze_logs.sh
    log_info "Created analyze_logs.sh"
}

# Exercise 3: Process manager
process_manager() {
    log_info "Creating process manager..."
    cat > manage_process.sh << 'EOF'
#!/bin/bash
# manage_process.sh - Start/stop/restart a process

set -euo pipefail

PID_FILE="/tmp/myapp.pid"
COMMAND="sleep 1000"  # Replace with actual command

start() {
    if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        log_warn "Process already running (PID: $(cat "$PID_FILE"))"
        return 1
    fi
    
    $COMMAND &
    echo $! > "$PID_FILE"
    log_info "Started process (PID: $!)"
}

stop() {
    if [[ ! -f "$PID_FILE" ]]; then
        log_warn "PID file not found"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        log_info "Stopped process (PID: $PID)"
    else
        log_warn "Process not running"
    fi
    rm -f "$PID_FILE"
}

restart() {
    stop
    sleep 1
    start
}

case "${1:-}" in
    start) start ;;
    stop) stop ;;
    restart) restart ;;
    status)
        if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            log_info "Running (PID: $(cat "$PID_FILE"))"
        else
            log_info "Not running"
        fi
        ;;
    *) echo "Usage: $0 {start|stop|restart|status}" ;;
esac
EOF
    chmod +x manage_process.sh
    log_info "Created manage_process.sh"
}

# Exercise 4: Deployment script
deploy_script() {
    log_info "Creating deployment script..."
    cat > deploy.sh << 'EOF'
#!/bin/bash
# deploy.sh - Simple deployment script

set -euo pipefail

APP_NAME="myapp"
VERSION="${1:-latest}"
ENV="${2:-staging}"

log_info() { echo "[INFO] $*"; }
log_error() { echo "[ERROR] $*" >&2; }

main() {
    log_info "Deploying $APP_NAME:$VERSION to $ENV"
    
    # Validate environment
    case "$ENV" in
        staging|production) ;;
        *) log_error "Invalid environment: $ENV"; exit 1 ;;
    esac
    
    # Build
    log_info "Building application..."
    go build -o "$APP_NAME" ./cmd/main.go
    
    # Test
    log_info "Running tests..."
    go test ./...
    
    # Deploy (simulated)
    log_info "Deploying to $ENV..."
    # scp "$APP_NAME" "user@$ENV-server:/opt/$APP_NAME/"
    # ssh "user@$ENV-server" "systemctl restart $APP_NAME"
    
    log_info "Deployment complete!"
}

main "$@"
EOF
    chmod +x deploy.sh
    log_info "Created deploy.sh"
}

# Run all exercises
main() {
    log_info "Creating shell scripting exercises..."
    backup_script
    log_analyzer
    process_manager
    deploy_script
    
    log_info "All scripts created in current directory:"
    ls -la *.sh
    
    log_info "Try running them:"
    echo "  ./backup.sh /path/to/source /path/to/dest"
    echo "  ./analyze_logs.sh /var/log/syslog ERROR"
    echo "  ./manage_process.sh start"
    echo "  ./deploy.sh v1.0.0 staging"
}

main "$@"