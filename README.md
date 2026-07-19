# Antigravity Updater

An open-source, automated updater for the Google Antigravity ecosystem (Hub, IDE, and CLI).

## Features

* **Multi-Language UI**: Automatically detects the system locale and displays the UI in either English or Traditional Chinese (`zh_TW`, `zh_CN`, `zh_HK`).
* **Hot-Swapping**: Safely replaces active installations without killing active language server processes, preventing session crashes.
* **Sandbox Fixes**: Automatically configures the `.desktop` launchers with the `--no-sandbox` parameter required for Linux user-local Electron installations.
* **Nautilus Integration**: Native support for the GNOME Nautilus file manager right-click context menu.

## Prerequisites

* Linux (x86_64 or arm64)
* Python 3
* `zenity` (Standard on GNOME, used for the graphical progress bars and dialogs)

## Installation (Nautilus Context Menu)

To use the updater directly from your file manager's right-click menu:

1. Clone or download this repository.
2. Link the script into your Nautilus scripts directory:
   ```bash
   mkdir -p ~/.local/share/nautilus/scripts/
   ln -s "$(pwd)/update.py" ~/.local/share/nautilus/scripts/Update\ Antigravity
   chmod +x ~/.local/share/nautilus/scripts/Update\ Antigravity
   ```

## Usage

### Method 1: Nautilus File Manager (Recommended)
1. Download an Antigravity `.tar.gz` package (e.g., `Antigravity.tar.gz` or `Antigravity IDE.tar.gz`).
2. Right-click the downloaded file in the file manager.
3. Select **Scripts -> Update Antigravity**.
4. The GUI will guide you through the rest.

### Method 2: Command Line
You can run the script from the terminal:
```bash
# To select a file via GUI:
./update.py

# To update a specific file directly:
./update.py /path/to/Antigravity.tar.gz
```

## How It Works
Instead of using traditional `kill` signals that might lock up your active IDE sessions, this script uses an atomic directory renaming technique (`safe_replace_directory`). It renames the active directory, extracts the new version, and allows the active memory processes to safely exit on their own time. The new version is automatically loaded the next time you start the app.
