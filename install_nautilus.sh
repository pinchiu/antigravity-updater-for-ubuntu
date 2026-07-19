#!/bin/bash
set -e

# 0. 防止使用 sh 執行（BASH_SOURCE 在 POSIX sh 中不可用）
if [ -z "${BASH_SOURCE+x}" ]; then
    echo "Please run this script with bash, not sh."
    echo "  bash install_nautilus.sh"
    exit 1
fi

echo "========================================="
echo "  Antigravity Nautilus Script Installer  "
echo "========================================="
echo ""

# 1. 阻擋 Root (sudo) 執行
# 如果使用 sudo 執行，腳本會被安裝到 /root/.local/... 而不是當前使用者的家目錄
if [ "$(id -u)" = "0" ]; then
    echo "Error: Do not run this script as root or with sudo."
    echo "錯誤：請不要使用 root 或 sudo 執行此腳本。"
    echo "   Nautilus scripts must be installed under your normal user's home directory."
    echo "   Nautilus 右鍵選單腳本必須安裝在您一般使用者的家目錄下。"
    exit 1
fi

# 2. 檢查必要依賴套件 (python3, zenity)
MISSING_DEPS=0
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 not found. / 錯誤：找不到 python3。"
    MISSING_DEPS=1
fi

if ! command -v zenity >/dev/null 2>&1; then
    echo "Error: zenity not found. / 錯誤：找不到 zenity (圖形化對話框工具)。"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -ne 0 ]; then
    echo ""
    echo "Please install the missing packages first. Example (Ubuntu/Debian):"
    echo "請先安裝缺失的系統套件。例如（以 Ubuntu/Debian 為例）："
    echo "  sudo apt install python3 zenity"
    exit 1
fi

# 3. 檢查 Nautilus 是否存在（僅提示，不阻擋，因為使用者可能正在遠端設定環境）
if ! command -v nautilus >/dev/null 2>&1; then
    echo "Warning: Nautilus file manager not found in PATH."
    echo "警告：系統中似乎未安裝 Nautilus 檔案管理員，或者未在 PATH 中。"
    echo "   (This script is designed for GNOME Nautilus; it may not work in other environments.)"
    echo "   (此腳本主要專為 GNOME Nautilus 右鍵選單設計，其他環境可能無效)"
    echo ""
fi

# 4. 精準獲取絕對路徑
# 確保不管使用者是透過拖曳 (drag and drop)、bash 還是 ./ 執行，都能準確抓到 update.py
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
UPDATE_SCRIPT="$DIR/update.py"

if [ ! -f "$UPDATE_SCRIPT" ]; then
    echo "Error: Cannot find update.py in $DIR"
    echo "錯誤：在 $DIR 中找不到 update.py"
    echo "   Please make sure you did not move install_nautilus.sh out of the repository folder."
    echo "   請確認您沒有單獨將 install_nautilus.sh 移出該資料夾。"
    exit 1
fi

# 5. 確保資料夾與權限正確
TARGET_DIR="$HOME/.local/share/nautilus/scripts"
TARGET_LINK="$TARGET_DIR/Update Antigravity"

echo "Installing Nautilus context menu script..."
echo "正在安裝 Nautilus 右鍵選單指令碼..."
mkdir -p "$TARGET_DIR"

# 強制建立軟連結 (若已存在舊連結或檔案，會直接覆蓋)
ln -sf "$UPDATE_SCRIPT" "$TARGET_LINK"

# 確保來源 python 腳本具備可執行權限
chmod +x "$UPDATE_SCRIPT"

echo ""
echo "Done! / 安裝成功！"
echo "   Symlink created at: $TARGET_LINK"
echo "   已將捷徑建立於: $TARGET_LINK"
echo ""
echo "   Right-click any .tar.gz file -> Scripts -> Update Antigravity"
echo "   對著任何 .tar.gz 檔案點擊右鍵 -> 腳本 (Scripts) -> Update Antigravity"
echo ""
echo "   (If the menu item doesn't appear, close and reopen your file manager.)"
echo "   (如果右鍵選單沒有出現，請關閉所有檔案管理員視窗後重新開啟即可。)"

