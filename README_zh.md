# Antigravity 更新器

一個開源、自動化的 Google Antigravity 生態系統更新工具（支援 Antigravity 與 Antigravity IDE）。

### 為什麼有這個專案？
在 Linux 系統上，Antigravity 官方的更新機制非常不便。每次有新版推出時，使用者都必須手動下載、手動解壓縮、手動覆蓋舊檔案並調整設定，這對一般使用者來說非常繁瑣且麻煩。

為了解決這個痛點，本專案提供了一個全自動化的解決方案。

您只要設定好此腳本，未來的更新流程就只需要：
1. 前往官網下載最新版的 `.tar.gz` 壓縮檔：
   - 若要更新 **Antigravity 2.0 (主程式)**：請下載 `Antigravity.tar.gz`
   - 若要更新 **Antigravity IDE**：請下載 `Antigravity IDE.tar.gz`
2. 對著該壓縮檔點擊**右鍵**，選擇 **指令碼 (Scripts) -> Update Antigravity**。
3. 程式即會自動幫您完成所有升級步驟（支援 `Antigravity 2.0` 與 `Antigravity IDE`）。

## 功能特點

* **多語言介面**：自動偵測系統語系，提供英文與繁體中文介面（簡體中文語系預設會以繁體中文顯示）。
* **熱更新 (Hot-Swapping)**：安全地替換現有安裝，無需強制關閉正在運作中的語言伺服器處理程序，防止開發環境當機。
* **沙盒修正**：自動設定 `.desktop` 啟動器，加入 Linux 系統下本機 Electron 安裝所需的 `--no-sandbox` 參數。
* **Nautilus 整合**：原生支援 GNOME Nautilus 檔案管理員的右鍵選單操作。
* **安全解壓縮**：防止在解壓縮 tar 壓縮檔時發生路徑穿越 (Path-Traversal / Zip-Slip) 攻擊。

## 安裝路徑

本更新器會自動將應用程式安裝（或更新）至 Linux 標準的使用者本機目錄下：
* **Antigravity**：`~/.local/share/antigravity/`（執行檔連結：`~/.local/bin/antigravity`）
* **Antigravity IDE**：`~/.local/share/antigravity-ide/`（執行檔連結：`~/.local/bin/antigravity-ide`）

> [!NOTE]
> 如果您先前是直接在自訂資料夾（例如 `~/Downloads`）手動解壓縮並執行 Antigravity，您有以下兩種方式可以遷移到標準本機路徑：
>
> * **選項一：透過更新自動遷移（推薦）**
>   1. 下載最新版的 `.tar.gz` 壓縮檔。
>   2. 直接使用本更新器執行該壓縮檔，更新器會自動將程式安裝至標準本機路徑（`~/.local/share/...`）。
>   3. 成功後，手動刪除您在 `~/Downloads` 底下的舊資料夾即可。
>
> * **選項二：手動搬移現有資料夾**
>   1. 手動將現有的程式資料夾移動到標準本機路徑：
>      * 例如：將 `~/Downloads/Antigravity IDE` 剪下並貼上至 `~/.local/share/antigravity-ide`
>   2. 執行一次更新器（選取當前或新版本的壓縮檔），以重新產生桌面啟動器捷徑，並更新執行檔連結。

## 系統需求

* Linux (x86_64 或 arm64)
* Python 3
* `zenity`（GNOME 的標準元件，用於顯示圖形化進度條與對話方塊）

## 安裝方式（Nautilus 右鍵選單）

> [!NOTE]
> **什麼是 Nautilus？** Nautilus 是以 GNOME 桌面環境為主的 Linux 系統（例如 Ubuntu、Debian、Fedora）所預設的圖形化檔案管理員，其功能與定位等同於 Windows 的「檔案總管」或 macOS 的「Finder」。

> [!IMPORTANT]
> **Nautilus 右鍵選單整合** 僅適用於使用 **GNOME 桌面環境** 且預設檔案管理員為 **Nautilus** 的 Linux 系統。若您使用的是 KDE (Dolphin)、XFCE (Thunar) 或其他桌面環境，請改用使用說明中的 **方式二** 或 **方式三**。

### 1. 安裝系統依賴項目
請確保您的系統已安裝 Python 3 和 Zenity。Zenity 通常會預裝在 GNOME 系統中，如果缺失可以手動安裝：
* **Ubuntu/Debian**: `sudo apt install python3 zenity`
* **Fedora**: `sudo dnf install python3 zenity`

### 2. 設定右鍵選單指令碼
為了簡化安裝流程，我們提供了一個自動化安裝腳本。
您可以直接在終端機中輸入 `bash `，然後將 `install_nautilus.sh` 拖曳到終端機內並按下 Enter；或者手動執行以下指令：

```bash
cd antigravity-updater
bash install_nautilus.sh
```
> [!TIP]
> 該腳本會自動偵測所在資料夾的絕對路徑並幫您建立好軟連結，您無須再擔心之前因為路徑不正確導致捷徑失效的問題。

## 使用方法

### 方式一：Nautilus 檔案管理員（推薦）
這是最簡單的更新方式。在設定好 Nautilus 腳本後：
1. 前往官網下載最新版的壓縮檔：
   - 若要更新 **Antigravity 2.0**：請下載 `Antigravity.tar.gz`
   - 若要更新 **Antigravity IDE**：請下載 `Antigravity IDE.tar.gz`
2. 在檔案管理員中，對著下載好的檔案點擊「右鍵」。
3. 選擇 **指令碼 (Scripts) -> Update Antigravity**。
4. 圖形介面會自動啟動，並顯示進度條引導您完成更新。

### 方式二：終端機執行（圖形介面模式）
您可以直接在終端機執行該指令碼，不帶任何參數。這將啟動檔案選擇視窗：
```bash
./update.py
```
隨後會彈出一個檔案選擇器，讓您手動選取下載好的 `.tar.gz` 壓縮檔。

### 方式三：終端機執行（直接指定檔案）
如果您不想透過檔案選擇器，也可以直接將壓縮檔的路徑作為參數傳遞給腳本：
```bash
./update.py ~/Downloads/Antigravity.tar.gz
```

## 運作原理 (熱更新)
此腳本並未使用傳統的 `kill` 指令強制終止程序（這可能導致開發階段的 IDE 當機），而是採用了原子化目錄重命名技術 (`safe_replace_directory`)。
它會先將目前正在使用的目錄重新命名，然後將新版本解壓縮到原本的位置，讓記憶體中正在運作的舊版處理程序能在它們自己的時間內安全結束。下次啟動應用程式時，系統就會自動載入最新的版本。

此外，它還會自動更新系統的桌面快取 (`update-desktop-database`)，以確保您的應用程式啟動圖示和捷徑路徑始終指向正確的最新版本。
