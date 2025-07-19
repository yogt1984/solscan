# SolScan

**SolScan** is a cloud-native, AI-enhanced agent framework for detecting, evaluating, and trading newly launched tokens on the Solana blockchain.

## 🎯 Project Mission
To autonomously identify profitable token generation events on Solana by combining:
- Real-time token detection
- On-chain health and safety evaluation
- Tick-based entropy and price action analysis
- Optional agent-driven trade execution based on learned profitability patterns

This system leverages Solana's unique advantages (high throughput and low fees) to enable predictive, autonomous, and data-rich token trading in the first 15 minutes of a launch.

## ✅ Core Modules

### 1. `token_detector.py`
- Uses the Helius API to detect new SPL token mint events and liquidity pool creations
- Outputs mint addresses, timestamps, and token age in minutes

### 2. `health_checker.py`
- Calls RugCheck.xyz, Birdeye, and other APIs to check:
  - Honeypot behavior
  - Buy/sell taxes
  - Ownership renouncement
  - LP lock status

### 3. `price_tracker.py`
- Streams price and volume data from Birdeye or Jupiter
- Computes tick entropy over short windows (e.g., 1m, 3m, 5m)
- Tracks early price delta and volatility

### 4. `agent_core.py` *(Planned)*
- Executes trades when conditions are met
- Tracks PnL and halts execution on loss thresholds
- Modular decision logic to be powered by XGBoost, LSTM, or Transformer-based classifiers

## 🧠 AI Agent Design
A cloud-hosted AI model will:
- Ingest early trade and token data
- Engineer features such as entropy, holder delta, and volume surges
- Train models to predict profitability
- Continuously learn and improve using feedback from real trades

## 🔌 External Integrations
- [Helius](https://www.helius.xyz) – Token mint detection
- [RugCheck.xyz](https://rugcheck.xyz) – Safety scanner
- [Birdeye](https://birdeye.so) – Real-time price and tick data
- [Jupiter Aggregator](https://jup.ag) – Slippage/routing and price data

## 💡 Technical Rationale
Solana is chosen due to:
- Extremely low transaction costs (fractions of a cent)
- High transaction throughput
- Fast block finality
- Ecosystem rich in newly launching tokens and fast market dynamics

## 📦 Estimated Codebase Size
Approx. 20,000 lines of Python and Rust, depending on:
- Backtesting module complexity
- Feature engineering depth
- Cloud deployment strategy

## 📍 Current Status
**Good news: I've decided to write this code.**
Development begins now, starting with:
- Real-time token detection module
- Health check integration

---

## 💬 Future Plans
- Deploy an AVM-compatible version of the tool
- Publish health + entropy as callable services in decentralized agent networks
- Expand to multi-agent strategies and execution benchmarking

---

Stay tuned. Contributions welcome once the scaffolding is in place.

