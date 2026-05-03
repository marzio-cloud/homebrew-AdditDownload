# AdditDownloader 📦

AdditDownloader is a fast, command-line utility that allows users to add, download, and install apps (window_casks). 

## ✨ Features
* **Add:** Add new apps to the public registry.
* **Download:** Fetch and download apps seamlessly.
* **Install Window:** Install a graphical window version of the app.

## 🚀 Usage

Run the tool via the command line:

```bash
# Add a new app to the list
python addit.py add <app_name> <download_url>

# Download an app
python addit.py download <app_name>

# Install the window/GUI app
python addit.py install-window <app_name>

---

### 💻 2. The Core CLI Script (`addit.py`)

Here is a boilerplate Python script using the built-in `argparse` library. This will handle the commands you requested: `-Download`, `-Add`, and `-Install window`.

```python
import argparse
import json
import os

# A simple local file to act as our database of added apps
REGISTRY_FILE = 'registry.json'

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_registry(data):
    with open(REGISTRY_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_app(name, url):
    registry = load_registry()
    registry[name] = {"url": url}
    save_registry(registry)
    print(f"✅ Successfully added '{name}' to the AdditDownloader registry!")

def download_app(name):
    registry = load_registry()
    if name in registry:
        url = registry[name]['url']
        print(f"⬇️ Downloading '{name}' from {url}...")
        # Future code to actually fetch the file goes here
        print(f"🎉 Download complete!")
    else:
        print(f"❌ Error: '{name}' not found. Please add it first.")

def install_window(name):
    print(f"🖼️ Setting up the window cask for '{name}'...")
    # Future code to extract and launch the app window goes here
    print(f"✅ '{name}' window installed successfully!")

def main():
    parser = argparse.ArgumentParser(description="AdditDownloader - Manage and download window_casks.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: add
    parser_add = subparsers.add_parser("add", help="Add a new app to the registry")
    parser_add.add_argument("name", help="The name of the app")
    parser_add.add_argument("url", help="The download URL for the app")

    # Command: download
    parser_download = subparsers.add_parser("download", help="Download an app")
    parser_download.add_argument("name", help="The name of the app to download")

    # Command: install-window
    parser_install = subparsers.add_parser("install-window", help="Install the windowed app")
    parser_install.add_argument("name", help="The name of the app to install as a window")

    args = parser.parse_args()

    if args.command == "add":
        add_app(args.name, args.url)
    elif args.command == "download":
        download_app(args.name)
    elif args.command == "install-window":
        install_window(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
