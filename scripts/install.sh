#!/bin/bash

# structure.sh installer
# This script downloads and installs the structure tool

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing structure.sh...${NC}"

# Create directory if it doesn't exist
mkdir -p "$HOME/.local/bin"

# Download the structure script
echo -e "Downloading structure tool..."
curl -s https://structure.sh/structure.py -o "$HOME/.local/bin/structure.py"
chmod +x "$HOME/.local/bin/structure.py"

# Create a wrapper script called 'structure'
cat > "$HOME/.local/bin/structure" << 'EOF'
#!/bin/bash

# structure - Directory structure visualization tool
# A wrapper for structure.py

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not found."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Parse command line arguments
OUTPUT_FILE="structure.txt"
DIRECTORY="."
IGNORE=""
SHARE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -i|--ignore)
            IGNORE="$2"
            shift 2
            ;;
        -s|--share)
            SHARE=true
            shift
            ;;
        -h|--help)
            echo "Usage: structure [options] [directory]"
            echo ""
            echo "Options:"
            echo "  -o, --output FILE    Write output to FILE (default: structure.txt)"
            echo "  -i, --ignore DIRS    Comma-separated list of directories to ignore"
            echo "  -s, --share          Generate a shareable URL at structure.sh"
            echo "  -h, --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  structure                      # Map current directory"
            echo "  structure /path/to/dir         # Map specific directory"
            echo "  structure -o output.txt        # Specify output file"
            echo "  structure -i node_modules,dist # Ignore additional directories"
            echo "  structure -s                   # Generate shareable URL"
            exit 0
            ;;
        *)
            DIRECTORY="$1"
            shift
            ;;
    esac
done

# Run the structure.py script
python3 "$HOME/.local/bin/structure.py" "$DIRECTORY" "$OUTPUT_FILE" "$IGNORE"

# Display the output file contents
if [ -f "$OUTPUT_FILE" ]; then
    echo ""
    cat "$OUTPUT_FILE"
    echo ""
    echo "Structure has been saved to $OUTPUT_FILE"
    
    # If share option is enabled, upload to server
    if [ "$SHARE" = true ]; then
        echo ""
        echo "Generating shareable link..."
        PROJECT_NAME=$(basename "$(realpath "$DIRECTORY")")
        SHARE_URL=$(curl -s -F "content=@$OUTPUT_FILE" -F "project=$PROJECT_NAME" https://structure.sh/api/share)
        
        if [[ $SHARE_URL == https://structure.sh/* ]]; then
            echo -e "${GREEN}Shareable link: $SHARE_URL${NC}"
        else
            echo "Error generating shareable link. Please try again later."
        fi
    fi
fi
EOF

chmod +x "$HOME/.local/bin/structure"

# Check if ~/.local/bin is in PATH, if not add it
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
    
    echo -e "${GREEN}Added $HOME/.local/bin to your PATH in .bashrc and .zshrc${NC}"
    echo "Please restart your terminal or run 'source ~/.bashrc' to update your PATH."
fi

# Check if installation was successful
if [ -f "$HOME/.local/bin/structure" ] && [ -f "$HOME/.local/bin/structure.py" ]; then
    echo -e "${GREEN}✓ structure.sh has been successfully installed!${NC}"
    echo ""
    echo "You can now run 'structure' in any directory to visualize its structure."
    echo "Examples:"
    echo "  structure                      # Map current directory"
    echo "  structure /path/to/dir         # Map specific directory"
    echo "  structure -o output.txt        # Specify output file"
    echo "  structure -i node_modules,dist # Ignore additional directories"
    echo "  structure -s                   # Generate shareable URL"
else
    echo "Error: Installation failed. Please check the error messages above."
fi
