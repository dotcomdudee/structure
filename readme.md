# Structure.sh

**Generate shareable directory trees in one command**

[Demo](https://structure.sh) • [Installation](#installation) • [Usage](#usage) • [Options](#options) • [Examples](#examples) • [Contributing](#contributing)

---

## ✨ Features

- 🌲 **Clean Directory Trees**: Generate clean and organized visualizations of your project structure
- 🔗 **Instant Sharing**: Create shareable URLs with a single command
- 🚀 **Simple to Use**: Just one command to generate a tree of any directory
- 🔧 **Customizable**: Ignore specific directories, customize output locations
- 🖥️ **Cross-Platform**: Works on macOS, Linux, and WSL
- 📋 **Project Documentation**: Perfect for READMEs, wikis, and documentation
- 🔄 **Automatic Updates**: Stay up-to-date with the latest features

## 📋 Overview

`structure.sh` is a simple tool that generates a clean visual representation of your directory structure. It's perfect for documentation, READMEs, or just getting a better overview of your project. With the sharing feature, you can instantly generate a URL to share your project structure with others.

## 🚀 Installation

### One-Line Install (macOS and Linux)

```bash
curl -s https://structure.sh/install | bash
```

That's it! The installer will:
1. Download the necessary files
2. Set up the `structure` command
3. Make it available in your PATH

### Manual Installation

If you prefer to install manually:

1. Clone the repository:
   ```bash
   git clone https://github.com/dotcomdudee/structure
   ```

2. Move to your local bin directory:
   ```bash
   cp structure.sh/structure.py ~/.local/bin/
   cp structure.sh/structure ~/.local/bin/
   chmod +x ~/.local/bin/structure.py
   chmod +x ~/.local/bin/structure
   ```

3. Make sure `~/.local/bin` is in your PATH

## 💻 Usage

### Basic Usage

Generate a tree visualization of the current directory:

```bash
structure
```

Output will be saved to `structure.txt` and displayed in your terminal.

### Sharing Your Structure

Generate a shareable URL for your project structure:

```bash
structure -s
```

This will:
1. Create the tree visualization
2. Upload it to structure.sh
3. Give you a unique URL you can share with anyone

### Command Structure

```
structure [options] [directory]
```

## ⚙️ Options

| Option | Description |
|--------|-------------|
| `-o, --output FILE` | Write output to FILE (default: structure.txt) |
| `-i, --ignore DIRS` | Comma-separated list of directories to ignore |
| `-s, --share` | Generate a shareable URL at structure.sh |
| `-h, --help` | Show help message |

## 📝 Examples

### Map Current Directory

```bash
structure
```

### Map Specific Directory

```bash
structure /path/to/project
```

### Specify Output File

```bash
structure -o project-structure.txt
```

### Ignore Specific Directories

```bash
structure -i node_modules,dist,build
```

### Share Your Project Structure

```bash
structure -s
```

This will output a URL like `https://structure.sh/abcd-efgh-ijkl-mnop`

### Example Output

```
my-project/
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
└── .gitignore
```

## 🔗 Sharing Features

The sharing functionality of structure.sh provides several benefits:

- **Persistent URLs**: Share once, reference anywhere
- **Clean Formatting**: Directory trees display correctly on any device
- **No Copy-Paste Issues**: Avoid formatting problems when pasting into documents
- **Quick Sharing**: Perfect for GitHub issues, pull requests, and documentation
- **Dark Mode Support**: Comfortable viewing in any environment

## 🔄 Updating

To update to the latest version:

```bash
curl -s https://structure.sh/install | bash
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgements

- Inspired by the `tree` command
- Thanks to all contributors who have helped shape this project

---

Made with ❤️ by dotcomdude