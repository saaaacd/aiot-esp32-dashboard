import streamlit as st
import sqlite3
import pandas as pd
import time
import datetime
import random

st.set_page_config(page_title="AIoT 即時儀表板", layout="wide")

DB_NAME = "aiotdb.db"

def load_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM sensors ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def generate_random_data():
    if 'random_data' not in st.session_state:
        st.session_state['random_data'] = []
        for i in range(100):
            t = datetime.datetime.now() - datetime.timedelta(seconds=2*(99-i))
            st.session_state['random_data'].append({
                'id': i+1,
                'temp': round(random.uniform(20.0, 35.0), 2),
                'humid': round(random.uniform(40.0, 80.0), 2),
                'metadata': '{"device_id": "Random_Sim"}',
                'timestamp': t.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    # Add new row
    last_id = st.session_state['random_data'][-1]['id'] if st.session_state['random_data'] else 0
    st.session_state['random_data'].append({
        'id': last_id + 1,
        'temp': round(random.uniform(20.0, 35.0), 2),
        'humid': round(random.uniform(40.0, 80.0), 2),
        'metadata': '{"device_id": "Random_Sim"}',
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Keep only last 100
    st.session_state['random_data'] = st.session_state['random_data'][-100:]
    
    df = pd.DataFrame(st.session_state['random_data'])
    # Return reversed order like the DB query
    return df.iloc[::-1].reset_index(drop=True)

st.title("ESP32 感測器即時儀表板")

st.markdown("---")
data_source = st.radio(
    "選擇資料來源：",
    ("🔌 ESP32 真實上傳資料", "🎲 系統隨機產生資料"),
    horizontal=True
)
st.markdown("---")

placeholder = st.empty()

while True:
    if data_source == "🔌 ESP32 真實上傳資料":
        df = load_data()
    else:
        df = generate_random_data()
    
    with placeholder.container():
        if not df.empty:
            latest = df.iloc[0]
            
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric(label="最新溫度 (°C)", value=f"{latest['temp']} °C")
            with kpi2:
                st.metric(label="最新濕度 (%)", value=f"{latest['humid']} %")
            with kpi3:
                st.metric(label="總紀錄筆數", value=len(df))
                
            disp_df = df.rename(columns={'id': '編號', 'temp': '溫度', 'humid': '濕度', 'metadata': '裝置資訊', 'timestamp': '時間戳記'})
                
            st.subheader("近期數據表")
            st.dataframe(disp_df.head(10))
            
            st.subheader("溫度趨勢圖 (°C)")
            st.line_chart(disp_df[['時間戳記', '溫度']].set_index('時間戳記').iloc[::-1])
            
            st.subheader("濕度趨勢圖 (%)")
            st.line_chart(disp_df[['時間戳記', '濕度']].set_index('時間戳記').iloc[::-1])
        else:
            st.warning("線上版本僅供介面展示，即時硬體連動需於本地執行")
            
    time.sleep(2)
