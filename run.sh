#!/bin/bash

# Navigate to script directory (in case it's run from elsewhere)
cd "$(dirname "$0")"

# Define paths
FRONTEND_DIR="./client"
FRONTEND_BUILD="./public"

# Check if React is built
if [ ! -d "$FRONTEND_BUILD" ]; then
    echo "⚡ Building React UI..."
    cd "$FRONTEND_DIR" || exit
    npm install
    npm run build
    cd ..
    mv "$FRONTEND_DIR/dist" "$FRONTEND_BUILD"
else
    echo "✅ React UI is already built."
fi

# Start Flask
echo "🚀 Starting Flask server..."
python3 app.py
