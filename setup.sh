#!/bin/zsh

set -e  # Stop the script on any command failure

# Function to handle errors
handle_error() {
    echo "\033[0;31mError: $1\033[0m"
    exit 1
}

# Step 1: Check if Python and necessary packages are installed
echo "Checking for Python..."
if ! command -v python3 &> /dev/null; then
    handle_error "Python3 not found. Please install it before running this script."
fi

# Step 2: Create a virtual environment if it doesn't already exist
if [ ! -d ".venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv .venv || handle_error "Failed to create virtual environment."
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Activate the virtual environment
source .venv/bin/activate || handle_error "Failed to activate virtual environment."

# Step 3: Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install --requirement requirements.txt --exists-action=w || handle_error "Failed to install Python dependencies."

# Step 4: Build C++ extension with cmake only if needed
echo "Checking C++ extension build..."
if [ ! -d "build" ]; then
    echo "Creating build directory and compiling C++ extension..."
    mkdir -p build && cd build || handle_error "Failed to create build directory."
    cmake -DPYTHON_EXECUTABLE=$(which python3) .. || handle_error "CMake configuration failed."
    make || handle_error "Failed to compile C++ extension."
    cd ..
else
    echo "Build directory already exists. Skipping compilation."
fi

# Step 5: Check Tesseract installation and add to .env file
echo "Checking for Tesseract OCR installation..."
if ! command -v tesseract &> /dev/null; then
    handle_error "Tesseract OCR is not installed. Please install it and ensure it is in your PATH."
fi

tesseract_path=$(which tesseract)
echo "Tesseract OCR found at $tesseract_path."

# Write the TESSERACT_PATH to a .env file
echo "Writing TESSERACT_PATH to .env file..."
echo "TESSERACT_PATH=$tesseract_path" > .env || handle_error "Failed to write TESSERACT_PATH to .env file."

# Step 6: Complete setup
echo "\033[0;32mSetup complete! Activate the environment with 'source .venv/bin/activate' and run main.py to start the project.\033[0m"