#!/usr/bin/env python3
import os
import sys
import tempfile
from urllib import request
from urllib.parse import urlencode
from urllib.request import Request
import json

# ANSI color codes for pretty output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

def generate_tree(directory, prefix="", is_last=True, ignore_dirs=None, use_colors=True):
    """
    Generate a tree structure for the given directory.
    
    Args:
        directory (str): The directory to map
        prefix (str): The prefix to use for the current line
        is_last (bool): Whether this is the last item in the current directory
        ignore_dirs (list): List of directory names to ignore
        use_colors (bool): Whether to use colors in the output
        
    Returns:
        str: The formatted tree structure
    """
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules']
    
    output = []
    plain_output = []  # Store output without color codes for sharing
    
    # Add the directory name
    base_name = os.path.basename(directory)
    if prefix == "":
        # Root directory
        if use_colors:
            output.append(f"{Colors.BOLD}{Colors.BLUE}{base_name}/{Colors.RESET}")
        else:
            output.append(f"{base_name}/")
        plain_output.append(f"{base_name}/")
        new_prefix = ""
    else:
        # Non-root directory
        if is_last:
            if use_colors:
                output.append(f"{prefix}└── {Colors.BLUE}{base_name}/{Colors.RESET}")
            else:
                output.append(f"{prefix}└── {base_name}/")
            plain_output.append(f"{prefix}└── {base_name}/")
            new_prefix = prefix + "    "
        else:
            if use_colors:
                output.append(f"{prefix}├── {Colors.BLUE}{base_name}/{Colors.RESET}")
            else:
                output.append(f"{prefix}├── {base_name}/")
            plain_output.append(f"{prefix}├── {base_name}/")
            new_prefix = prefix + "│   "
    
    # List all items in the directory
    try:
        items = sorted([item for item in os.listdir(directory) 
                      if not item.startswith('.') or item == '.env.example'])
        
        # Filter out ignored directories
        filtered_items = []
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and item in ignore_dirs:
                continue
            filtered_items.append(item)
        
        # Process directories first, then files
        dirs = [item for item in filtered_items if os.path.isdir(os.path.join(directory, item))]
        files = [item for item in filtered_items if not os.path.isdir(os.path.join(directory, item))]
        
        all_items = dirs + files
        
        for i, item in enumerate(all_items):
            item_path = os.path.join(directory, item)
            is_current_last = (i == len(all_items) - 1)
            
            if os.path.isdir(item_path):
                # It's a directory, recurse into it
                colored_subtree, plain_subtree = generate_tree(item_path, new_prefix, is_current_last, ignore_dirs, use_colors)
                output.extend(colored_subtree)
                plain_output.extend(plain_subtree)
            else:
                # It's a file - apply color based on file type
                ext = os.path.splitext(item)[1].lower()
                file_color = get_file_color(ext) if use_colors else ""
                reset = Colors.RESET if use_colors else ""
                
                if is_current_last:
                    if use_colors:
                        output.append(f"{new_prefix}└── {file_color}{item}{reset}")
                    else:
                        output.append(f"{new_prefix}└── {item}")
                    plain_output.append(f"{new_prefix}└── {item}")
                else:
                    if use_colors:
                        output.append(f"{new_prefix}├── {file_color}{item}{reset}")
                    else:
                        output.append(f"{new_prefix}├── {item}")
                    plain_output.append(f"{new_prefix}├── {item}")
    
    except PermissionError:
        if use_colors:
            output.append(f"{new_prefix}├── {Colors.RED}Access Denied{Colors.RESET}")
        else:
            output.append(f"{new_prefix}├── Access Denied")
        plain_output.append(f"{new_prefix}├── Access Denied")
    except Exception as e:
        if use_colors:
            output.append(f"{new_prefix}├── {Colors.RED}Error: {str(e)}{Colors.RESET}")
        else:
            output.append(f"{new_prefix}├── Error: {str(e)}")
        plain_output.append(f"{new_prefix}├── Error: {str(e)}")
    
    return output, plain_output

def get_file_color(extension):
    """Return color code based on file extension"""
    # Source code files
    if extension in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.cs', '.go', '.rb', '.php']:
        return Colors.GREEN
    # Markup/config files
    elif extension in ['.html', '.xml', '.css', '.json', '.yml', '.yaml', '.toml', '.ini', '.conf']:
        return Colors.CYAN
    # Documentation files
    elif extension in ['.md', '.txt', '.rst', '.pdf', '.doc', '.docx']:
        return Colors.YELLOW
    # Image files
    elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp']:
        return Colors.MAGENTA
    # Executable/binary files
    elif extension in ['.exe', '.dll', '.so', '.dylib', '.bin']:
        return Colors.RED
    # Default
    else:
        return Colors.WHITE

def share_structure(content, project_name):
    """
    Share the structure content with structure.sh and get a shareable URL.
    
    Args:
        content (str): The tree structure content
        project_name (str): The name of the project
        
    Returns:
        str: The shareable URL or error message
    """
    try:
        # Create a temporary file with the content
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp:
            temp.write(content)
            temp_path = temp.name
        
        # Prepare the multipart form data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        }
        
        # Format the multipart form data
        data = []
        data.append(f'--{boundary}'.encode())
        data.append(f'Content-Disposition: form-data; name="project"'.encode())
        data.append(''.encode())
        data.append(project_name.encode())
        data.append(f'--{boundary}'.encode())
        data.append(f'Content-Disposition: form-data; name="content"; filename="{os.path.basename(temp_path)}"'.encode())
        data.append(f'Content-Type: text/plain'.encode())
        data.append(''.encode())
        
        with open(temp_path, 'rb') as f:
            data.append(f.read())
        
        data.append(f'--{boundary}--'.encode())
        data.append(''.encode())
        
        body = '\r\n'.encode().join(data)
        
        # Make the request
        req = Request('https://structure.sh/api/share', data=body, headers=headers)
        with request.urlopen(req) as response:
            if response.status == 200:
                return response.read().decode('utf-8')
            else:
                return f"Error: Received status code {response.status}"
    
    except Exception as e:
        return f"Error sharing structure: {str(e)}"
    finally:
        # Clean up the temporary file
        if 'temp_path' in locals():
            os.unlink(temp_path)

def main():
    # Parse command line arguments
    directory = "."
    ignore = ""
    share = False
    use_colors = True
    project_name = os.path.basename(os.path.abspath(directory))
    
    # Process args
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ["-i", "--ignore"]:
            if i + 1 < len(args):
                ignore = args[i + 1]
                i += 2
            else:
                i += 1
        elif args[i] in ["-s", "--share"]:
            share = True
            i += 1
        elif args[i] in ["-p", "--project"]:
            if i + 1 < len(args):
                project_name = args[i + 1]
                i += 2
            else:
                i += 1
        elif args[i] in ["--no-color"]:
            use_colors = False
            i += 1
        elif args[i] in ["-h", "--help"]:
            print("Usage: structure-direct [options] [directory]")
            print("")
            print("Options:")
            print("  -i, --ignore DIRS    Comma-separated list of directories to ignore")
            print("  -s, --share          Generate a shareable URL")
            print("  -p, --project NAME   Project name for sharing (default: directory name)")
            print("  --no-color           Disable colored output")
            print("  -h, --help           Show this help message")
            print("")
            print("Examples:")
            print("  curl -s https://structure.sh/direct | python3                     # Current directory")
            print("  curl -s https://structure.sh/direct | python3 - /path/to/dir      # Specific directory")
            print("  curl -s https://structure.sh/direct | python3 - -i node_modules   # Ignore directories")
            print("  curl -s https://structure.sh/direct | python3 - -s                # Share structure")
            sys.exit(0)
        else:
            directory = args[i]
            project_name = os.path.basename(os.path.abspath(directory))
            i += 1
    
    # Check if we're running in a terminal that supports colors
    if not sys.stdout.isatty():
        use_colors = False
    
    # Parse ignore dirs
    if ignore:
        custom_ignore = ignore.split(',')
        ignore_dirs = ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules'] + custom_ignore
    else:
        ignore_dirs = ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules']
    
    # Generate the tree structure
    colored_tree, plain_tree = generate_tree(directory, ignore_dirs=ignore_dirs, use_colors=use_colors)
    colored_content = '\n'.join(colored_tree)
    plain_content = '\n'.join(plain_tree)
    
    # Print the result with fancy header if colors are enabled
    if use_colors:
        print(f"\n{Colors.BOLD}{Colors.GREEN}╭───── Directory Structure ─────╮{Colors.RESET}")
        print(colored_content)
        print(f"{Colors.BOLD}{Colors.GREEN}╰───────────────────────────────╯{Colors.RESET}\n")
    else:
        print(plain_content)
    
    # Share if requested
    if share:
        print(f"\n{Colors.CYAN}Generating shareable link...{Colors.RESET}" if use_colors else "\nGenerating shareable link...")
        share_url = share_structure(plain_content, project_name)
        
        if use_colors:
            print(f"{Colors.BOLD}Shareable link:{Colors.RESET} {Colors.GREEN}{share_url}{Colors.RESET}")
        else:
            print(f"Shareable link: {share_url}")

if __name__ == "__main__":
    main()