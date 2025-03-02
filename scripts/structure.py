#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def generate_tree(directory, prefix="", is_last=True, ignore_dirs=None):
    """
    Generate a tree structure for the given directory.
    
    Args:
        directory (str): The directory to map
        prefix (str): The prefix to use for the current line
        is_last (bool): Whether this is the last item in the current directory
        ignore_dirs (list): List of directory names to ignore
        
    Returns:
        str: The formatted tree structure
    """
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules']
    
    output = []
    
    # Add the directory name
    base_name = os.path.basename(directory)
    if prefix == "":
        # Root directory
        output.append(f"{base_name}/")
        new_prefix = ""
    else:
        # Non-root directory
        if is_last:
            output.append(f"{prefix}└── {base_name}/")
            new_prefix = prefix + "    "
        else:
            output.append(f"{prefix}├── {base_name}/")
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
                output.extend(generate_tree(item_path, new_prefix, is_current_last, ignore_dirs))
            else:
                # It's a file
                if is_current_last:
                    output.append(f"{new_prefix}└── {item}")
                else:
                    output.append(f"{new_prefix}├── {item}")
    
    except PermissionError:
        output.append(f"{new_prefix}├── Access Denied")
    except Exception as e:
        output.append(f"{new_prefix}├── Error: {str(e)}")
    
    return output

def main():
    """
    Main function to generate a directory structure and save it to a file.
    """
    # Get the directory to map
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = os.getcwd()
    
    # Get output file name
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "structure.txt"
    
    # Get custom ignore directories
    if len(sys.argv) > 3 and sys.argv[3]:
        custom_ignore = sys.argv[3].split(',')
        ignore_dirs = ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules'] + custom_ignore
    else:
        ignore_dirs = ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules']
    
    # Generate the tree structure
    tree_structure = generate_tree(root_dir, ignore_dirs=ignore_dirs)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(tree_structure))
    
    print(f"Directory structure has been saved to {output_file}")

if __name__ == "__main__":
    main()