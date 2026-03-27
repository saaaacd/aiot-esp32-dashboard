<h1 align="center">IoT Sensor Live Dashboard 📊</h1>

<p align="center">
  一個以 Flask + Streamlit 打造，結合 ESP32 開發板與 SQLite 輕量資料庫的「人工智慧物聯網 (AIoT)」專題示範系統。
</p>

---

## 🚀 專案簡介
本專案示範如何透過 **ESP32 實體開發板** 收集感測器數據（如溫濕度），並使用 `HTTP POST` 的方式將 JSON 資料上傳至後端 Python 伺服器，接著將資料持久化存入 **SQLite3** 資料庫中，最後再搭配 **Streamlit** 提供一個具備科技質感的深色主題「即時監控儀表板」。

本專案支援兩種資料來源，可於儀表板上方無縫切換：
1. **🔌 ESP32 真實上傳資料**
2. **🎲 系統隨機產生資料**（供沒有硬體時進行 UI 開發測試）

---

## 📂 專案架構
| 檔案名稱 / 目錄 | 功能說明 |
| :--- | :--- |
| `app.py` | Flask 後端伺服器 (Port 5000)，負責任聽 `/sensor` 位址並寫入資料庫。 |
| `dashboard.py` | Streamlit 即時前端儀表板，每 2 秒自動刷新最新的歷史溫濕度曲線。 |
| `esp32_sim.py` | 開發用的軟體模擬器，能自動發送隨機假數據至 Flask，方便本機端壓力測試。 |
| `aiotdb.db` | SQLite 資料庫檔案 (由 `app.py` 自動建立及維護)。 |
| `wifi_mysql_test.ino` | 提供給 ESP32 的 Arduino 韌體 C++ 程式碼。 |
| `requirements.txt` | Python 環境的必要套件清單。 |
| `.streamlit/config.toml` | 儀表板深色/主題自訂外觀設定檔。 |

---

## 🛠️ 環境配置與安裝

### 1. 安裝 Python 依賴套件
為避免套件衝突，建議建立虛擬環境 (`venv`)：
```bash
python -m venv venv
# 啟動虛擬環境 (Windows)
.\venv\Scripts\activate
# 啟動虛擬環境 (Mac/Linux)
# source venv/bin/activate

# 安裝所需套件
pip install -r requirements.txt
```

### 2. 啟動這套系統
必須開兩個終端機視窗，分別執行：

**終端機 1：啟動後端 Flask API (Port 5000)**
```bash
python app.py
```

**終端機 2：啟動前端 Streamlit 儀表板 (Port 8501)**
```bash
streamlit run dashboard.py
```

如果你沒有 ESP32 開發板，你可以開啟第三個終端機執行模擬器：
```bash
python esp32_sim.py
```

---

## 🔌 ESP32 實體開發板配置
如果想要連結你自己手邊的硬體，請打開 `wifi_mysql_test/wifi_mysql_test.ino`：
1. 更改 Wi-Fi 的 `ssid` 和 `password`。
2. 將 `serverName` 變更為你電腦在區網內的 IP 位址（例如：`http://192.168.0.x:5000/sensor`）。
3. 使用 Arduino IDE 將程式碼燒錄至 ESP32 後即可在儀表板即時看見數據跳動！

---

## 🛡️ License
This project is for educational and AIoT demonstration purposes. 
