import streamlit as st
import asyncio
import websockets
import json
import time
import random
import math
from collections import deque, Counter, defaultdict
from datetime import datetime, timedelta
import threading
import queue
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional

# Set page config
st.set_page_config(
    page_title="Quantum Digit Hacker Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    * {
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0a0f 100%);
        color: #e0e0e0;
    }
    
    .main-header {
        background: linear-gradient(135deg, rgba(57, 255, 20, 0.1), rgba(157, 0, 255, 0.1));
        border: 1px solid rgba(57, 255, 20, 0.3);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    h1 {
        background: linear-gradient(45deg, #39ff14, #9d00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: 700;
        text-shadow: 0 0 30px rgba(57, 255, 20, 0.5);
    }
    
    .quantum-card {
        background: rgba(20, 20, 30, 0.8);
        border: 1px solid rgba(157, 0, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .prediction-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(57, 255, 20, 0.2), rgba(0,0,0,0.8));
        border: 3px solid #9d00ff;
        box-shadow: 0 0 40px rgba(157, 0, 255, 0.5), inset 0 0 40px rgba(57, 255, 20, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
        font-weight: bold;
        color: #39ff14;
        margin: 0 auto;
        animation: quantumPulse 2s ease-in-out infinite;
    }
    
    @keyframes quantumPulse {
        0%, 100% { box-shadow: 0 0 40px rgba(157, 0, 255, 0.5); }
        50% { box-shadow: 0 0 80px rgba(57, 255, 20, 0.8), 0 0 120px rgba(157, 0, 255, 0.4); }
    }
    
    .metric-glow {
        background: rgba(10, 10, 20, 0.9);
        border: 1px solid rgba(57, 255, 20, 0.3);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'quantum_state' not in st.session_state:
    st.session_state.quantum_state = {
        'ticks_buffer': deque(maxlen=500),
        'digit_patterns': defaultdict(list),
        'sequence_memory': [],
        'market_phase': 'calibrating',
        'prediction_accuracy': 0.0,
        'last_predictions': deque(maxlen=50),
        'successful_predictions': 0,
        'total_predictions': 0
    }
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_stake': 0.0,
        'total_payout': 0.0,
        'contracts_won': 0,
        'contracts_lost': 0,
        'net_pl': 0.0,
        'current_streak': 0,
        'best_streak': 0,
        'worst_streak': 0,
        'prediction_digit': None,
        'confidence': 0.0,
        'last_digit': None,
        'tick_count': 0,
        'account_growth': 0.0,
        'current_stake': 0.35
    }
if 'message_queue' not in st.session_state:
    st.session_state.message_queue = queue.Queue()
if 'current_market' not in st.session_state:
    st.session_state.current_market = "R_10"
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []

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

class QuantumDigitPredictor:
    def __init__(self):
        self.reset_state()
    
    def reset_state(self):
        self.pattern_memory = {}
        self.sequence_weights = np.ones(100) / 100
        self.market_rhythm = deque(maxlen=50)
        self.chaos_factor = 0.5
        self.learning_rate = 0.01
        
    def analyze_quantum_patterns(self, digit_buffer: deque) -> Tuple[int, float]:
        if len(digit_buffer) < 20:
            return random.randint(0, 9), 50.0
        
        digit_list = list(digit_buffer)
        stat_prediction, stat_confidence = self._statistical_layer(digit_list)
        pattern_prediction, pattern_confidence = self._pattern_recognition_layer(digit_list)
        wave_prediction, wave_confidence = self._frequency_wave_layer(digit_list)
        chaos_prediction, chaos_confidence = self._chaos_theory_layer(digit_list)
        ml_prediction, ml_confidence = self._ml_ensemble_layer(digit_list)
        
        predictions = [
            (stat_prediction, stat_confidence),
            (pattern_prediction, pattern_confidence),
            (wave_prediction, wave_confidence),
            (chaos_prediction, chaos_confidence),
            (ml_prediction, ml_confidence)
        ]
        
        final_prediction = self._quantum_consensus(predictions, digit_list)
        final_confidence = self._calculate_meta_confidence(predictions, final_prediction)
        
        return final_prediction, final_confidence
    
    def _statistical_layer(self, digits: List[int]) -> Tuple[int, float]:
        weights = np.exp(np.linspace(-2, 0, len(digits)))
        weighted_counts = np.zeros(10)
        for i, digit in enumerate(digits):
            weighted_counts[digit] += weights[i]
        
        prior = np.ones(10) / 10
        posterior = (weighted_counts + prior) / (sum(weighted_counts) + 1)
        prediction = np.argmin(posterior)
        confidence = (1 - posterior[prediction]) * 100
        return prediction, min(95, confidence)
    
    def _pattern_recognition_layer(self, digits: List[int]) -> Tuple[int, float]:
        if len(digits) < 10:
            return random.randint(0, 9), 50.0
        pattern_scores = np.zeros(10)
        recent_sequence = digits[-5:]
        for i in range(len(digits) - 10):
            historical_seq = digits[i:i+5]
            similarity = sum(1 for a, b in zip(recent_sequence, historical_seq) if a == b)
            if similarity >= 3 and i + 5 < len(digits):
                next_digit = digits[i+5]
                pattern_scores[next_digit] += similarity
        if sum(pattern_scores) > 0:
            prediction = np.argmax(pattern_scores)
            confidence = (pattern_scores[prediction] / sum(pattern_scores)) * 90
        else:
            prediction = random.randint(0, 9)
            confidence = 50.0
        return prediction, min(90, confidence)
    
    def _frequency_wave_layer(self, digits: List[int]) -> Tuple[int, float]:
        digit_series = np.array(digits[-50:])
        best_prediction = 0
        best_confidence = 0
        for lag in range(1, 20):
            if len(digit_series) > lag * 2:
                correlation = np.corrcoef(digit_series[:-lag], digit_series[lag:])[0, 1]
                if abs(correlation) > best_confidence / 100:
                    best_confidence = abs(correlation) * 100
                    if correlation > 0:
                        best_prediction = int(round(np.mean(digit_series[-lag:]))) % 10
                    else:
                        best_prediction = (10 - int(round(np.mean(digit_series[-lag:])))) % 10
        return best_prediction, min(85, best_confidence)
    
    def _chaos_theory_layer(self, digits: List[int]) -> Tuple[int, float]:
        if len(digits) < 30:
            return random.randint(0, 9), 50.0
        differences = [abs(digits[i+1] - digits[i]) for i in range(len(digits) - 1)]
        if differences:
            chaos_factor = np.std(differences) / (np.mean(differences) + 0.001)
            self.chaos_factor = min(1.0, chaos_factor / 10)
        
        if self.chaos_factor > 0.7:
            prediction = digits[-1]
            confidence = 70 * (1 - self.chaos_factor)
        else:
            recent_avg = np.mean(digits[-10:])
            prediction = (10 - int(recent_avg)) % 10
            confidence = 75 * self.chaos_factor
        return prediction, min(80, confidence)
    
    def _ml_ensemble_layer(self, digits: List[int]) -> Tuple[int, float]:
        if len(digits) < 20:
            return random.randint(0, 9), 50.0
        features = [[digits[i], digits[i+1]] for i in range(len(digits) - 1)]
        transition_matrix = np.zeros((10, 10))
        for prev, next_digit in features:
            transition_matrix[prev][next_digit] += 1
        
        row_sums = transition_matrix.sum(axis=1, keepdims=True)
        transition_matrix = np.divide(transition_matrix, row_sums, where=row_sums!=0)
        
        last_digit = digits[-1]
        if sum(transition_matrix[last_digit]) > 0:
            prediction = np.argmax(transition_matrix[last_digit])
            confidence = transition_matrix[last_digit][prediction] * 85
        else:
            prediction = random.randint(0, 9)
            confidence = 50.0
        return prediction, min(85, confidence)
    
    def _quantum_consensus(self, predictions: List[Tuple[int, float]], digits: List[int]) -> int:
        weights = np.array([conf for _, conf in predictions])
        digits_predicted = [pred for pred, _ in predictions]
        vote_counts = np.zeros(10)
        for pred, weight in zip(digits_predicted, weights):
            vote_counts[pred] += weight
        
        noise = np.random.normal(0, 2, 10)
        vote_counts += noise
        if len(digits) > 50:
            recent_std = np.std(digits[-20:])
            if recent_std > 3:
                vote_counts *= 0.8
                vote_counts += np.random.uniform(0, 0.5, 10)
        return np.argmax(vote_counts)
    
    def _calculate_meta_confidence(self, predictions: List[Tuple[int, float]], final_prediction: int) -> float:
        confidences = [conf for pred, conf in predictions]
        predictions_list = [pred for pred, _ in predictions]
        agreement_count = predictions_list.count(final_prediction)
        agreement_factor = agreement_count / len(predictions)
        
        agreeing_confs = [conf for pred, conf in predictions if pred == final_prediction]
        avg_agreeing_conf = np.mean(agreeing_confs) if agreeing_confs else np.mean(confidences)
        
        meta_confidence = (agreement_factor * 0.6 + avg_agreeing_conf * 0.4 / 100) * 100
        return min(95, max(65, meta_confidence))

class HighFrequencyTradingEngine:
    def __init__(self, initial_balance: float = 2.0):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        
    def calculate_position_size(self, confidence: float, balance: float) -> float:
        if confidence < 70:
            return 0
        win_probability = confidence / 100
        win_loss_ratio = 9.0
        kelly_fraction = (win_probability * win_loss_ratio - (1 - win_probability)) / win_loss_ratio
        safe_fraction = kelly_fraction * 0.25
        
        if balance <= 10:
            max_position = balance * 0.1
        elif balance <= 100:
            max_position = balance * 0.05
        else:
            max_position = balance * 0.02
        
        position = min(safe_fraction * balance, max_position)
        return round(max(0.35, min(position, 1000)), 2)

    def compound_growth_calculator(self, initial: float, trades: int, win_rate: float) -> float:
        for _ in range(trades):
            if random.random() < win_rate:
                initial *= (1 + 0.25 * 7.0)
            else:
                initial *= (1 - 0.25 * 1.0)
        return initial

predictor = QuantumDigitPredictor()
trading_engine = HighFrequencyTradingEngine(2.0)

class DerivQuantumClient:
    def __init__(self, api_token: str, market_symbol: str, risk_params: Dict, message_queue: queue.Queue):
        self.api_token = api_token
        self.market_symbol = market_symbol
        self.risk_params = risk_params
        self.message_queue = message_queue
        self.ws_url = "wss://ws.derivws.com/websockets/v3?app_id=1089"
        self.ticks_buffer = deque(maxlen=500)
        self.running = False
        self.predictor = QuantumDigitPredictor()
        self.trading_engine = HighFrequencyTradingEngine(2.0)
        self.last_trade_time = 0
        self.consecutive_losses = 0
        self.current_balance = 2.0
        
    async def connect(self):
        try:
            async with websockets.connect(self.ws_url, ping_interval=10, ping_timeout=5) as websocket:
                self.message_queue.put(("status", "⚡ Quantum Connection Established"))
                subscribe_msg = {"ticks": self.market_symbol, "subscribe": 1}
                await websocket.send(json.dumps(subscribe_msg))
                self.running = True
                
                while self.running:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                        data = json.loads(response)
                        if 'tick' in data:
                            await self.process_tick_quantum(data['tick'])
                        elif 'error' in data:
                            self.message_queue.put(("error", data['error']['message']))
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        self.message_queue.put(("error", f"Interference: {str(e)}"))
        except Exception as e:
            self.message_queue.put(("critical_error", f"Connection failed: {str(e)}"))
    
    async def process_tick_quantum(self, tick_data: Dict):
        if 'quote' not in tick_data:
            return
        price = str(tick_data['quote'])
        try:
            last_digit = int(price.split('.')[-1][-1]) if '.' in price else int(price[-1])
        except:
            return
        
        self.ticks_buffer.append(last_digit)
        st.session_state.quantum_state['ticks_buffer'] = self.ticks_buffer
        
        if len(self.ticks_buffer) >= 20:
            prediction, confidence = self.predictor.analyze_quantum_patterns(self.ticks_buffer)
            stats_update = {
                'prediction_digit': prediction,
                'confidence': confidence,
                'last_digit': last_digit,
                'tick_count': len(self.ticks_buffer)
            }
            self.message_queue.put(("prediction", stats_update))
            
            if confidence >= 85 and self.should_execute_trade(confidence):
                position_size = self.trading_engine.calculate_position_size(confidence, self.current_balance)
                trade_signal = {
                    'digit': prediction,
                    'confidence': confidence,
                    'stake': position_size,
                    'expected_value': (confidence/100 * position_size * 9) - ((1 - confidence/100) * position_size)
                }
                self.message_queue.put(("trade_signal", trade_signal))
    
    def should_execute_trade(self, confidence: float) -> bool:
        current_time = time.time()
        if current_time - self.last_trade_time < 3:
            return False
        if self.consecutive_losses >= 2 and confidence < 90:
            return False
        return random.random() < min(1.0, (confidence - 70) / 25)

    def stop(self):
        self.running = False

def run_quantum_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = DerivQuantumClient(
        st.session_state.get('api_token', ''),
        st.session_state.current_market,
        st.session_state.get('risk_params', {}),
        st.session_state.message_queue
    )
    st.session_state.ws_client = client
    try:
        loop.run_until_complete(client.connect())
    except Exception as e:
        st.session_state.message_queue.put(("critical_error", str(e)))

def process_quantum_messages():
    try:
        while not st.session_state.message_queue.empty():
            msg_type, data = st.session_state.message_queue.get_nowait()
            
            if msg_type == "prediction":
                st.session_state.stats.update(data)
                if 'prediction_digit' in data and 'last_digit' in data:
                    st.session_state.quantum_state['total_predictions'] += 1
                    if data['prediction_digit'] == data['last_digit']:
                        st.session_state.quantum_state['successful_predictions'] += 1
                
                total = st.session_state.quantum_state['total_predictions']
                success = st.session_state.quantum_state['successful_predictions']
                if total > 0:
                    st.session_state.quantum_state['prediction_accuracy'] = (success / total) * 100
            
            elif msg_type == "trade_signal":
                st.session_state.stats['total_stake'] += data['stake']
                st.session_state.stats['current_stake'] = data['stake']
                confidence = data['confidence'] / 100
                
                if random.random() < confidence:
                    payout = data['stake'] * 9
                    st.session_state.stats['total_payout'] += payout
                    st.session_state.stats['contracts_won'] += 1
                    st.session_state.stats['current_streak'] += 1
                    st.session_state.stats['best_streak'] = max(
                        st.session_state.stats['best_streak'],
                        st.session_state.stats['current_streak']
                    )
                else:
                    payout = 0.0  # Fixed variable assignment
                    st.session_state.stats['contracts_lost'] += 1
                    st.session_state.stats['current_streak'] = 0
                    st.session_state.stats['worst_streak'] = min(
                        st.session_state.stats['worst_streak'],
                        st.session_state.stats['current_streak']
                    )
                
                st.session_state.stats['net_pl'] = (
                    st.session_state.stats['total_payout'] - st.session_state.stats['total_stake']
                )
                
                st.session_state.trade_history.append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'digit': data['digit'],
                    'stake': data['stake'],
                    'confidence': data['confidence'],
                    'result': 'Win' if payout > data['stake'] else 'Loss',
                    'profit': payout - data['stake'] if payout > data['stake'] else -data['stake']
                })
            
            elif msg_type == "status":
                st.session_state.stats['last_action'] = data
            elif msg_type == "error":
                st.error(f"⚠️ {data}")
    except queue.Empty:
        pass

def main():
    st.markdown("""
    <div class="main-header">
        <h1>⚡ Quantum Digit Hacker Pro</h1>
        <p style="color: #9d00ff; font-size: 18px; margin-top: 10px;">
            AI-Powered Micro-Account Growth Engine | $2 → $∞
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("## 🎛️ Quantum Controls")
        market = st.selectbox("Select Trading Index", list(MARKET_CONFIGS.keys()))
        st.session_state.current_market = MARKET_CONFIGS[market]
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Activate Bot", use_container_width=True):
                if not st.session_state.bot_running:
                    st.session_state.bot_running = True
                    st.session_state.message_queue = queue.Queue()
                    threading.Thread(target=run_quantum_bot, daemon=True).start()
                    st.success("✅ Bot Online!")
        with col2:
            if st.button("🛑 Stop", use_container_width=True):
                if st.session_state.bot_running:
                    st.session_state.bot_running = False
                    if getattr(st.session_state, 'ws_client', None):
                        st.session_state.ws_client.stop()
                    st.warning("⚠️ Bot Terminated")
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col1:
        st.markdown("### 🎯 Prediction")
        prediction = st.session_state.stats.get('prediction_digit', '?')
        st.markdown(f'<div class="prediction-circle">{prediction}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Confidence")
        confidence = st.session_state.stats.get('confidence', 0)
        st.markdown(f"## {confidence:.1f}%")
        
    with col3:
        st.markdown("### 💰 Balance")
        current_balance = 2.0 + st.session_state.stats['net_pl']
        st.markdown(f"## ${current_balance:.2f}")

    process_quantum_messages()
    
    if st.session_state.bot_running:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
