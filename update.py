#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import tarfile
import tempfile
import subprocess
import time
import locale
import inspect

# --- i18n Translation Dictionary ---
LANGUAGES = {
    "en": {
        "title": "Antigravity Updater",
        "file_picker_title": "Select the downloaded Antigravity archive (.tar.gz)",
        "unrecognized_file": "Unrecognized filename: {filename}\nPlease ensure the filename contains 'Antigravity' or 'IDE'.",
        "preparing": "Preparing update...",
        "extracting": "Extracting installation package...",
        "installing": "Installing files and setting up shortcuts...",

        "err_no_folder": "Could not find Antigravity directory in the archive",
        "err_no_ide_folder": "Could not find 'Antigravity IDE' directory in the archive",
        "updating_cache": "Updating desktop launcher cache...",
        "complete": "Update complete!",
        "success": "{product_name} has been successfully updated to the new version!\n\nIt will run the new version on the next launch (restart).",
        "error": "An error occurred during the update:\n{error_msg}"
    },
    "zh": {
        "title": "Antigravity 更新器",
        "file_picker_title": "選擇下載好的 Antigravity 壓縮檔 (.tar.gz)",
        "unrecognized_file": "無法識別的檔案名稱：{filename}\n請確保檔案名稱包含 'Antigravity' 或 'IDE'。",
        "preparing": "正在準備更新...",
        "extracting": "正在解壓縮安裝包...",
        "installing": "正在安裝檔案與設定捷徑...",

        "err_no_folder": "無法在壓縮包中找到 Antigravity 目錄",
        "err_no_ide_folder": "無法在壓縮包中找到 'Antigravity IDE' 目錄",
        "updating_cache": "正在更新桌面啟動器快取...",
        "complete": "更新完成！",
        "success": "{product_name} 已成功升級為新版！\n\n下次啟動（重啟）時即會以新版本運作。",
        "error": "更新過程中發生錯誤：\n{error_msg}"
    }
}

# Module-level language setting, initialized by detect_language()
current_lang = "en"

def detect_language():
    """Detect system language and set the module-level current_lang variable"""
    global current_lang
    try:
        sys_lang, _ = locale.getlocale()
    except Exception:
        sys_lang = None

    if not sys_lang:
        sys_lang = os.environ.get('LANG', 'en_US')

    # Default to English unless the locale starts with "zh"
    current_lang = "zh" if sys_lang and sys_lang.lower().startswith("zh") else "en"

def _(key, **kwargs):
    """Translation helper function"""
    text = LANGUAGES[current_lang].get(key, LANGUAGES["en"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text

def zenity_message(msg_type, text):
    """Show GUI prompt using Zenity"""
    subprocess.run(["zenity", f"--{msg_type}", "--text", text, "--title", _("title")], check=False)

def extract_asar_file(asar_path, target_file, dest_path):
    """Extract a single file from Electron asar archive without npm dependency"""
    import struct
    import json
    try:
        with open(asar_path, 'rb') as f:
            header_info = f.read(16)
            if len(header_info) < 16:
                return False
            uint_size, header_size, header_string_size, header_json_size = struct.unpack('<IIII', header_info)
            header_json = f.read(header_json_size).decode('utf-8')
            header = json.loads(header_json)
            
            node = header
            for part in target_file.strip('/').split('/'):
                if 'files' in node and part in node['files']:
                    node = node['files'][part]
                else:
                    return False
            
            if 'size' not in node or 'offset' not in node:
                return False
                
            size = node['size']
            offset = int(node['offset'])
            f.seek(header_size + 8 + offset)
            data = f.read(size)
            with open(dest_path, 'wb') as out:
                out.write(data)
            return True
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to extract {target_file} from ASAR: {e}\n")
        return False

def update_desktop_launchers():
    """Rebuild desktop launcher shortcuts to ensure correct links"""
    app_dir = os.path.expanduser("~/.local/share/applications")
    home = os.path.expanduser("~")
    os.makedirs(app_dir, exist_ok=True)
    
    # Antigravity desktop launcher (only if installed)
    hub_exe = f"{home}/.local/share/antigravity/antigravity"
    if os.path.exists(hub_exe):
        hub_desktop = os.path.join(app_dir, "antigravity.desktop")
        hub_icon = f"{home}/.local/share/antigravity/antigravity.png"
        if not os.path.exists(hub_icon):
            hub_icon = f"{home}/.local/share/antigravity/antigravity.svg"
            
        hub_content = f"""\
[Desktop Entry]
Name=Antigravity 2.0
Comment=Antigravity Desktop Application
Exec={home}/.local/share/antigravity/antigravity --no-sandbox %F
Icon={hub_icon}
Type=Application
Categories=Development;IDE;
Terminal=false
StartupWMClass=antigravity
"""
        try:
            with open(hub_desktop, "w", encoding="utf-8") as f:
                f.write(hub_content)
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to write Antigravity desktop launcher: {e}\n")
        
    # IDE desktop launcher (only if IDE is installed)
    ide_exe_primary = f"{home}/.local/share/antigravity-ide/bin/antigravity-ide"
    ide_exe_fallback = f"{home}/.local/share/antigravity-ide/antigravity-ide"
    if os.path.exists(ide_exe_primary) or os.path.exists(ide_exe_fallback):
        ide_desktop = os.path.join(app_dir, "antigravity-ide.desktop")
        ide_icon = f"{home}/.local/share/antigravity-ide/antigravity-ide.svg"
        if not os.path.exists(ide_icon):
            ide_icon = f"{home}/.local/share/antigravity/antigravity.png"
        if not os.path.exists(ide_icon):
            ide_icon = f"{home}/.local/share/antigravity/antigravity.svg"
            
        ide_content = f"""\
[Desktop Entry]
Name=Antigravity IDE
Comment=AI-First Integrated Development Environment
Exec={home}/.local/share/antigravity-ide/antigravity-ide --no-sandbox %F
Icon={ide_icon}
Type=Application
Categories=Development;IDE;
Terminal=false
StartupWMClass=antigravity-ide
"""
        try:
            with open(ide_desktop, "w", encoding="utf-8") as f:
                f.write(ide_content)
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to write IDE desktop launcher: {e}\n")
        
    # Update system cache
    try:
        subprocess.run(["update-desktop-database", app_dir], capture_output=True, check=False)
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to update desktop database: {e}\n")

def safe_replace_directory(src, dst):
    """Safely replace directory (using rename to avoid file lock conflicts, supporting hot updates)"""
    temp_old = None
    if os.path.exists(dst):
        temp_old = dst + ".old." + str(int(time.time()))
        try:
            shutil.move(dst, temp_old)
        except Exception as e:
            sys.stderr.write(f"Failed to move old directory: {e}\n")
            raise
            
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
    except Exception as e:
        if temp_old and os.path.exists(temp_old):
            try:
                shutil.move(temp_old, dst)
            except Exception:
                pass
        sys.stderr.write(f"Failed to move new directory into place: {e}\n")
        raise
    finally:
        if temp_old and os.path.exists(temp_old):
            try:
                shutil.rmtree(temp_old, ignore_errors=True)
            except Exception as e:
                sys.stderr.write(f"Warning: Failed to cleanup old directory: {e}\n")

def main():
    detect_language()
    
    # Get file paths
    selected_file = None
    
    # 1. Try to get from Nautilus environment variables first
    nautilus_paths = os.environ.get('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS')
    if nautilus_paths:
        paths = [p for p in nautilus_paths.split('\n') if p.strip()]
        if paths:
            selected_file = paths[0]
            
    # 2. Try to get from command line arguments
    if not selected_file and len(sys.argv) > 1:
        selected_file = sys.argv[1]
        
    # 3. If not provided, open file picker
    if not selected_file:
        try:
            res = subprocess.run(
                ["zenity", "--file-selection", "--file-filter=*.tar.gz", f"--title={_('file_picker_title')}"],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                selected_file = res.stdout.strip()
        except Exception as e:
            sys.stderr.write(f"Failed to open Zenity file picker: {e}\n")
            
    if not selected_file or not os.path.exists(selected_file):
        # User cancelled or file does not exist
        sys.exit(0)
        
    filename = os.path.basename(selected_file)
    
    # Determine product type
    product_type = None
    if "-ide" in filename.lower() or " ide" in filename.lower():
        product_type = "ide"
        product_name = "Antigravity IDE"
    elif "antigravity" in filename.lower():
        product_type = "app"
        product_name = "Antigravity"
    else:
        # Unrecognized filename
        zenity_message("error", _("unrecognized_file", filename=filename))
        sys.exit(1)

    # Open progress bar window
    progress = subprocess.Popen(
        ["zenity", "--progress", f"--title={_('title')}", f"--text={_('preparing')}", "--auto-close", "--percentage=0"],
        stdin=subprocess.PIPE, text=True
    )
    
    def set_progress(pct, text):
        try:
            progress.stdin.write(f"{pct}\n")
            progress.stdin.write(f"# {text}\n")
            progress.stdin.flush()
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to update progress bar: {e}\n")

    try:
        # 1. Extract files
        set_progress(20, _("extracting"))
        with tempfile.TemporaryDirectory() as tmpdir:
            with tarfile.open(selected_file, "r:gz") as tar:
                # Compatibility for different Python extraction filters
                sig = inspect.signature(tarfile.TarFile.extractall)
                if 'filter' in sig.parameters:
                    tar.extractall(path=tmpdir, filter='data')
                else:
                    # Fallback for older Python versions to prevent path traversal
                    for member in tar.getmembers():
                        member_path = os.path.abspath(os.path.join(tmpdir, member.name))
                        if not member_path.startswith(os.path.abspath(tmpdir)):
                            raise Exception("Path traversal attempt detected in tarball")
                    tar.extractall(path=tmpdir)

            set_progress(60, _("installing"))
            
            # Set installation target paths
            app_dir = os.path.expanduser("~/.local/share/antigravity")
            app_link = os.path.expanduser("~/.local/bin/antigravity")
            ide_dir = os.path.expanduser("~/.local/share/antigravity-ide")
            ide_link = os.path.expanduser("~/.local/bin/antigravity-ide")

            if product_type == "app":
                extracted_folder = None
                for item in os.listdir(tmpdir):
                    full_path = os.path.join(tmpdir, item)
                    if os.path.isdir(full_path) and item.startswith("Antigravity"):
                        extracted_folder = full_path
                        break
                
                if not extracted_folder:
                    raise FileNotFoundError(_("err_no_folder"))
                
                # Safe hot update
                safe_replace_directory(extracted_folder, app_dir)
                
                # Recreate shortcut links
                target_exe = os.path.join(app_dir, "antigravity")
                if os.path.exists(target_exe):
                    os.chmod(target_exe, 0o755)
                    if os.path.exists(app_link) or os.path.islink(app_link):
                        os.remove(app_link)
                    os.symlink(target_exe, app_link)

                # Extract icon from ASAR
                asar_path = os.path.join(app_dir, "resources", "app.asar")
                if os.path.exists(asar_path):
                    extract_asar_file(asar_path, "icon.png", os.path.join(app_dir, "antigravity.png"))

            elif product_type == "ide":
                extracted_folder = os.path.join(tmpdir, "Antigravity IDE")
                if not os.path.exists(extracted_folder):
                    raise FileNotFoundError(_("err_no_ide_folder"))
                
                # Safe hot update
                safe_replace_directory(extracted_folder, ide_dir)
                
                # Recreate shortcut links
                target_exe = os.path.join(ide_dir, "bin", "antigravity-ide")
                if not os.path.exists(target_exe):
                    target_exe = os.path.join(ide_dir, "antigravity-ide")
                
                if os.path.exists(target_exe):
                    os.chmod(target_exe, 0o755)
                    if os.path.exists(ide_link) or os.path.islink(ide_link):
                        os.remove(ide_link)
                    os.symlink(target_exe, ide_link)

                # Copy icon from internal resources
                src_icon = os.path.join(ide_dir, "resources", "app", "out", "vs", "platform", "browserOnboarding", "static", "antigravity.svg")
                if os.path.exists(src_icon):
                    try:
                        shutil.copy(src_icon, os.path.join(ide_dir, "antigravity-ide.svg"))
                    except Exception as e:
                        sys.stderr.write(f"Warning: Failed to copy IDE icon: {e}\n")

        # 2. Rebuild desktop shortcuts
        set_progress(80, _("updating_cache"))
        update_desktop_launchers()
        
        set_progress(100, _("complete"))
        progress.stdin.close()
        try:
            progress.wait(timeout=5)
        except subprocess.TimeoutExpired:
            progress.kill()
        
        # Success prompt
        zenity_message("info", _("success", product_name=product_name))

    except Exception as e:
        try:
            progress.stdin.close()
            progress.wait(timeout=5)
        except Exception:
            pass
        zenity_message("error", _("error", error_msg=str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()
