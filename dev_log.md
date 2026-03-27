# AIoT Project Development Log

## Setup Process
1. Created `app.py` for the Flask backend.
2. Created `esp32_sim.py` for the simulated ESP32 device.
3. Created `dashboard.py` for the Streamlit dashboard.
4. Set up an isolated Python virtual environment (`venv`).
5. Installed all required dependencies (`Flask`, `requests`, `streamlit`, `pandas`).

## How to Run the Demo Locally

1. **Activate the Virtual Environment**:
   ```bash
   .\venv\Scripts\activate
   ```

2. **Run Flask Backend**:
   ```bash
   python app.py
   ```
   *Expected URL*: http://127.0.0.1:5000/health

3. **Run ESP32 Simulator**:
   ```bash
   python esp32_sim.py
   ```
   *Note: This will output sent data every 5 seconds.*

4. **Run Streamlit Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```
   *Expected URL*: http://localhost:8501

## Live Demo (Vercel / Streamlit Cloud)
To deploy this project:
1. Push this directory to a GitHub repository.
2. Go to **[Streamlit Community Cloud](https://share.streamlit.io/)** and create a new app pointing to `dashboard.py`.
3. The app will automatically read from `aiotdb.db` (if uploaded) or start fresh. Note: A live backend (Flask) would also need to be deployed to a service like Render or PythonAnywhere to receive real ESP32 POST requests from the cloud.

---
*Log generated during local demo setup.*
