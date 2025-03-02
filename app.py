#!/usr/bin/env python3
import os
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, abort, send_from_directory

app = Flask(__name__)

# Configuration
SHARE_DB = "shares.db"
SHARES_DIR = "shares"
SCRIPTS_DIR = "scripts"

# Ensure directories exist
os.makedirs(SHARES_DIR, exist_ok=True)
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# Set up the database
def setup_db():
    conn = sqlite3.connect(SHARE_DB)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shares (
        id TEXT PRIMARY KEY,
        project_name TEXT,
        created_at TIMESTAMP,
        file_path TEXT,
        view_count INTEGER DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

setup_db()

# Generate a unique ID for sharing
def generate_share_id():
    return str(uuid.uuid4())

@app.route('/')
def index():
    """Render the main website."""
    return render_template('index.html')

@app.route('/install')
def serve_install():
    """Serve the install.sh script."""
    return send_from_directory(SCRIPTS_DIR, 'install.sh')

@app.route('/direct')
def serve_direct():
    """Serve the structure-direct.py script for no-install usage."""
    return send_from_directory(SCRIPTS_DIR, 'structure-direct.py')

@app.route('/structure.py')
def serve_structure_py():
    """Serve the structure.py script."""
    return send_from_directory(SCRIPTS_DIR, 'structure.py')

@app.route('/api/share', methods=['POST'])
def create_share():
    """API endpoint to create a new share."""
    if 'content' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['content']
    project_name = request.form.get('project', 'Unnamed Project')
    
    # Generate a unique ID
    share_id = generate_share_id()
    
    # Save the file
    file_path = os.path.join(SHARES_DIR, f"{share_id}.txt")
    file.save(file_path)
    
    # Store in database
    conn = sqlite3.connect(SHARE_DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO shares (id, project_name, created_at, file_path) VALUES (?, ?, ?, ?)",
        (share_id, project_name, datetime.now(), file_path)
    )
    conn.commit()
    conn.close()
    
    # Return the shareable URL
    share_url = f"https://structure.sh/{share_id}"
    return share_url

@app.route('/<share_id>')
def view_share(share_id):
    """View a shared directory structure."""
    # Check if it's a special route
    if share_id in ['favicon.ico', 'robots.txt']:
        return '', 404
    
    # Validate the ID format to prevent directory traversal
    if not all(c.isalnum() or c == '-' for c in share_id):
        return render_template('index.html')
    
    # Get share info from database
    conn = sqlite3.connect(SHARE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT project_name, file_path FROM shares WHERE id = ?", (share_id,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return render_template('index.html')
    
    project_name, file_path = result
    
    # Increment view count
    cursor.execute("UPDATE shares SET view_count = view_count + 1 WHERE id = ?", (share_id,))
    conn.commit()
    conn.close()
    
    # Read the file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return render_template('index.html')
    
    # Render the template with the content
    return render_template('view.html', 
                          project_name=project_name, 
                          content=content, 
                          share_id=share_id)

@app.route('/raw/<share_id>')
def raw_share(share_id):
    """Get the raw text content of a share."""
    # Special handling for demo
    if share_id == 'demo':
        demo_content = """sample-project/
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── Footer.js
│   │   └── Sidebar.js
│   ├── utils/
│   │   └── helpers.js
│   └── App.js
├── public/
│   ├── index.html
│   └── favicon.ico
├── tests/
│   └── App.test.js
├── package.json
├── README.md
└── .gitignore"""
        return demo_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    
    # Validate the ID format to prevent directory traversal
    if not all(c.isalnum() or c == '-' for c in share_id):
        abort(404)
    
    # Get file path from database
    conn = sqlite3.connect(SHARE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM shares WHERE id = ?", (share_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        abort(404)
    
    file_path = result[0]
    
    # Read the file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        abort(404)
    
    # Return as plain text
    return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/demo')
def demo():
    return render_template('view.html',
                          project_name="Demo",
                          content="""sample-project/
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── Footer.js
│   │   └── Sidebar.js
│   ├── utils/
│   │   └── helpers.js
│   └── App.js
├── public/
│   ├── index.html
│   └── favicon.ico
├── tests/
│   └── App.test.js
├── package.json
├── README.md
└── .gitignore""",
                          share_id="demo")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)