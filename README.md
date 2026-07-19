# Antigravity Updater

An open-source, automated updater for the Google Antigravity ecosystem (Antigravity and Antigravity IDE).

### Why This Project Exists
On Linux, the official update mechanism for Antigravity is far from ideal. Every time a new version is released, users must manually download, extract, replace the old files, and reconfigure settings, which is tedious and troublesome for most users.

To solve this pain point, this project provides a fully automated solution.

Once you have this script installed, updating is as simple as:
1. Download the latest `.tar.gz` archive from the official website:
   - To update **Antigravity 2.0 (Main App)**: download `Antigravity.tar.gz`
   - To update **Antigravity IDE**: download `Antigravity IDE.tar.gz`
2. Right-click the downloaded archive and choose **Scripts -> Update Antigravity**.
3. The script will automatically handle the entire upgrade process (supports upgrading both `Antigravity 2.0` and `Antigravity IDE`).

## Features

* **Multi-Language UI**: Automatically detects the system locale. Provides English and Traditional Chinese interfaces (Simplified Chinese locales will fall back to Traditional Chinese).
* **Hot-Swapping**: Safely replaces active installations without killing active language server processes, preventing session crashes.
* **Sandbox Fixes**: Automatically configures the `.desktop` launchers with the `--no-sandbox` parameter required for Linux user-local Electron installations.
* **Nautilus Integration**: Native support for the GNOME Nautilus file manager right-click context menu.
* **Secure Extraction**: Guards against zip-slip/path-traversal attacks when extracting tar archives.

## Installation Paths

The updater automatically installs (or updates) the applications to standard Linux user-local directories:
* **Antigravity**: `~/.local/share/antigravity/` (Binary link: `~/.local/bin/antigravity`)
* **Antigravity IDE**: `~/.local/share/antigravity-ide/` (Binary link: `~/.local/bin/antigravity-ide`)

> [!NOTE]
> If you previously ran Antigravity manually from a custom directory (like `~/Downloads`), you have two ways to migrate to the standard location:
>
> * **Option 1: Auto-Migration via Update (Recommended)**
>   1. Download the new `.tar.gz` archive.
>   2. Run this updater on it. The updater will automatically extract and install it in the standard location (`~/.local/share/...`).
>   3. Manually delete the old custom directory in `~/Downloads`.
>
> * **Option 2: Manual Migration of Existing Setup**
>   1. Manually move your existing program folder to the standard path:
>      * E.g., Move `~/Downloads/Antigravity IDE` to `~/.local/share/antigravity-ide`
>   2. Run this updater on any `.tar.gz` archive to recreate the desktop launchers and command shortcuts pointing to the new path.

## Prerequisites

* Linux (x86_64 or arm64)
* Python 3
* `zenity` (Standard on GNOME, used for the graphical progress bars and dialogs)

## Installation (Nautilus Context Menu)

> [!NOTE]
> **What is Nautilus?** Nautilus is the default graphical file manager on GNOME-based Linux distributions (such as Ubuntu, Debian, Fedora). It is the equivalent of "File Explorer" on Windows or "Finder" on macOS.

> [!IMPORTANT]
> **Nautilus Context Menu integration** only works on Linux systems using the **GNOME Desktop Environment** where **Nautilus** is the active file manager. If you use KDE (Dolphin), XFCE (Thunar), or another environment, please use **Method 2** or **Method 3** in the usage section instead.

### 1. Install Dependencies
Ensure you have Python 3 and Zenity installed. Zenity is typically pre-installed on GNOME systems, but you can install it manually if missing:
* **Ubuntu/Debian**: `sudo apt install python3 zenity`
* **Fedora**: `sudo dnf install python3 zenity`

### 2. Set Up the Context Menu Script
To make setup easier, we've included an automated installation script.
You can simply type `bash ` in your terminal, drag and drop the `install_nautilus.sh` file into the terminal window and press Enter, or run it manually:

```bash
cd antigravity-updater
bash install_nautilus.sh
```
> [!TIP]
> The script automatically resolves its absolute path and creates the correct symbolic links, completely eliminating the need for you to worry about running it from the exact right directory.

## Usage

### Method 1: Nautilus File Manager (Recommended)
This is the easiest way to update. Once you've set up the Nautilus script:
1. Download the latest archive from the official website:
   - To update **Antigravity 2.0**: download `Antigravity.tar.gz`
   - To update **Antigravity IDE**: download `Antigravity IDE.tar.gz`
2. Right-click the downloaded file in your file manager.
3. Select **Scripts -> Update Antigravity**.
4. The GUI will appear and guide you through the update process, showing a progress bar.

### Method 2: Command Line (GUI Mode)
You can run the script from the terminal without any arguments. It will prompt you to select the archive:
```bash
./update.py
```
A file picker will open allowing you to choose the `.tar.gz` file you downloaded.

### Method 3: Command Line (Direct Mode)
If you prefer not to use the file picker, you can pass the path to the downloaded archive directly as an argument:
```bash
./update.py /path/to/Antigravity.tar.gz
```

## How It Works (Hot Swapping)
Instead of using traditional `kill` signals that might lock up your active IDE sessions, this script uses an atomic directory renaming technique (`safe_replace_directory`). It renames the active directory, extracts the new version in its place, and allows the active memory processes to safely exit on their own time. The new version is automatically loaded the next time you start the app. 

Additionally, it automatically updates your system's desktop cache (`update-desktop-database`) to ensure your application launcher icons and paths are always pointing to the correct, latest version.
