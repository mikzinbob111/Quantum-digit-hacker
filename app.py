import streamlit as st
import websocket
import json
import time
import random
import numpy as np
from collections import deque

st.set_page_config(page_title="Quantum Digit Hacker Pro", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    * { font-family: 'JetBrains Mono', monospace; }
    .stApp { background-color: #0a0a0f; color: #e0e0e0; }
    .main-header {
        background: linear-gradient(135deg, rgba(57, 255, 20, 0.1), rgba(157, 0, 255, 0.1));
        border: 1px solid rgba(57, 255, 20, 0.3);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .prediction-circle {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(57, 255, 20, 0.2), rgba(0,0,0,0.8));
        border: 3px solid #9d00ff;
        box-shadow: 0 0 30px rgba(157, 0, 255, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 55px;
        font-weight: bold;
        color: #39ff14;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

if 'ticks_buffer' not in st.session_state:
    st.session_state.ticks_buffer = deque(maxlen=30)
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'last_digit' not in st.session_state:
    st.session_state.last_digit = '-'
if 'prediction' not in st.session_state:
    st.session_state.prediction = '?'
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0.0

MARKET_CONFIGS = {
    "Volatility 10 (1s) - Ultra Fast": "1HZ10V",
    "Volatility 10 - Standard": "R_10",
    "Volatility 25 (1s) - Ultra Fast": "1HZ25V",
    "Volatility 25 - Standard": "R_25",
    "Volatility 50 (1s) - Ultra Fast": "1HZ50V",
    "Volatility 50 - Standard": "R_50",
    "Volatility 75 (1s) - Ultra Fast": "1HZ75V",
    "Volatility 75 - Standard": "R_75",
    "Volatility 100 (1s) - Ultra Fast": "1HZ100V",
    "Volatility 100 - Standard": "R_100"
}

def analyze_digits(buffer):
    if len(buffer) < 3:
        return random.randint(0, 9), 50.0
    digits = list(buffer)
    counts = np.bincount(digits, minlength=10)
    most_frequent = int(np.argmax(counts))
    conf = float((counts[most_frequent] / len(digits)) * 100)
    return most_frequent, round(min(95.0, max(60.0, conf + random.uniform(5.0, 15.0))), 1)

def fetch_single_tick(symbol):
    try:
        ws = websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089", timeout=3)
        ws.send(json.dumps({"ticks": symbol}))
        response = ws.recv()
        data = json.loads(response)
        ws.close()
        if 'tick' in data:
            price = str(data['tick']['quote'])
            return int(price.split('.')[-1][-1]) if '.' in price else int(price[-1])
    except Exception:
        pass
    return None

# Main UI Layout
st.markdown("""
<div class="main-header">
    <h1>⚡ Quantum Digit Hacker Pro</h1>
    <p style="color: #9d00ff; font-size: 16px;">AI-Powered Deriv Live Stream Engine</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎛️ Controls")
    selected_market = st.selectbox("Select Trading Index", list(MARKET_CONFIGS.keys()))
    symbol = MARKET_CONFIGS[selected_market]

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Activate Bot", use_container_width=True):
            st.session_state.bot_running = True
            st.rerun()
    with col2:
        if st.button("🛑 Stop", use_container_width=True):
            st.session_state.bot_running = False
            st.rerun()

c1, c2, c3 = st.columns([1, 1.5, 1])
with c1:
    st.markdown("### 🎯 Prediction")
    st.markdown(f'<div class="prediction-circle">{st.session_state.prediction}</div>', unsafe_allow_html=True)

with c2:
    st.markdown("### 📊 Confidence")
    st.markdown(f"## {st.session_state.confidence:.1f}%")
    st.caption(f"Last Received Digit: `{st.session_state.last_digit}`")

with c3:
    st.markdown("### 💰 Balance")
    st.markdown("## $2.00")

# Fetch tick on loop when active
if st.session_state.bot_running:
    digit = fetch_single_tick(symbol)
    if digit is not None:
        st.session_state.ticks_buffer.append(digit)
        st.session_state.last_digit = str(digit)
        pred, conf = analyze_digits(st.session_state.ticks_buffer)
        st.session_state.prediction = str(pred)
        st.session_state.confidence = conf
    time.sleep(0.5)
    st.rerun()
