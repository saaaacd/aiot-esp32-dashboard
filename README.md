# AIoT Sensor Dashboard

這個專案是一個完整的 AIoT (人工智慧物聯網) 示範系統，包含三個主要部分：
1. **ESP32 實體開發板 (C++)**：透過 WiFi 與 HTTP POST 將 DHT11 溫濕度資料上傳。
2. **Flask 後端 API (Python)**：接收 ESP32 上傳的 JSON 資料並安全寫入 SQLite3 資料庫。
3. **Streamlit 即時儀表板 (Python)**：提供深色科技風格的美觀介面，即時讀取資料庫並產生圖表與數據監控。

## 專案架構
- `app.py` - Flask HTTP API (Port 5000) 與資料庫寫入邏輯。
- `dashboard.py` - Streamlit 網頁儀表板 (即時圖表與監控介面)。
- `esp32_sim.py` - Python 開發用的本機模擬器 (可模擬 ESP32 傳送假資料)。
- `wifi_mysql_test/wifi_mysql_test.ino` - 燒錄到 ESP32 開發板的 Arduino 程式碼 (發送 JSON 格式資料)。
- `requirements.txt` - Python 執行環境依賴套件清單。
- `.streamlit/config.toml` - Streamlit 儀表板深色/亮色主題與自訂紫色按鈕的設定檔。

## 如何在本地端執行
1. 安裝所需套件：
   ```bash
   pip install -r requirements.txt
   ```
2. 啟動 Flask 後端 API：
   ```bash
   python app.py
   ```
3. 啟動 Streamlit 儀表板：
   ```bash
   streamlit run dashboard.py
   ```
4. 燒錄 `.ino` 至 ESP32 開發板即可開始即時收集數據！
