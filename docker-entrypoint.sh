#!/bin/bash
set -e

# If the first argument is "--cli", run in CLI mode
if [ "$1" = "--cli" ]; then
    echo "Running in CLI mode..."
    exec python main.py --cli
fi

# Otherwise start the web server
echo "Starting web server..."
exec python main.py