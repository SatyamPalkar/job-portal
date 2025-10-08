#!/bin/bash

echo "🛑 Stopping Resume Optimizer..."

# Kill processes by PID file if exists
if [ -f .pids ]; then
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2>/dev/null && echo "   Stopped process $pid"
        fi
    done < .pids
    rm -f .pids
fi

# Kill any remaining processes
pkill -f "uvicorn backend.main" 2>/dev/null && echo "   Stopped backend"
pkill -f "vite" 2>/dev/null && echo "   Stopped frontend"

echo "✅ All servers stopped!"

