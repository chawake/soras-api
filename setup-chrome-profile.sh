#!/bin/bash
# Script to copy Chrome profile with ChatGPT session into Docker volume

set -e

echo "=== Sora API Chrome Profile Setup ==="
echo ""
echo "This script will help you set up your ChatGPT session for Sora API"
echo ""

# Check if volume exists
if ! docker volume ls | grep -q chrome_profile; then
    echo "Creating chrome_profile volume..."
    docker volume create chrome_profile
fi

# Get volume path
VOLUME_PATH=$(docker volume inspect chrome_profile --format '{{ .Mountpoint }}')
echo "Volume location: $VOLUME_PATH"
echo ""

echo "OPTIONS:"
echo "1. Copy from Windows Chrome profile"
echo "2. Manual setup (open Chrome in container)"
echo ""
read -p "Choose option (1 or 2): " option

if [ "$option" = "1" ]; then
    echo ""
    echo "Windows Chrome profile is usually at:"
    echo "C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    echo ""
    read -p "Enter full path to your Chrome profile: " PROFILE_PATH
    
    if [ ! -d "$PROFILE_PATH" ]; then
        echo "ERROR: Profile path not found!"
        exit 1
    fi
    
    echo "Copying profile..."
    # This would need to be run on Windows or with WSL
    cp -r "$PROFILE_PATH"/* "$VOLUME_PATH/Default/"
    echo "✓ Profile copied successfully!"
    
elif [ "$option" = "2" ]; then
    echo ""
    echo "Starting container with Chrome..."
    echo "After Chrome opens, login to https://sora.chatgpt.com"
    echo "Your session will be saved automatically"
    echo ""
    read -p "Press Enter to start container..."
    
    # Run container with Chrome in headed mode (requires X11)
    docker run --rm -it \
        -v chrome_profile:/root/LLMProvider \
        -e DISPLAY=$DISPLAY \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        $(docker build -q .) \
        bash -c "google-chrome --user-data-dir=/root/LLMProvider"
else
    echo "Invalid option"
    exit 1
fi

echo ""
echo "=== Setup Complete ==="
echo "Your Chrome profile is now configured in the chrome_profile volume"
echo "Deploy to Coolify and it will use this session"
