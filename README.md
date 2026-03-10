# KalshiPulse — Insider Tracker

Monitor big trades, whale activity, and unusual flow on Kalshi prediction markets.

## Quick Start

### 1. Install dependencies
```bash
pip install flask flask-cors requests
```

### 2. Start the server
```bash
python server.py
```

### 3. Open the dashboard
Navigate to: **http://localhost:5000**

---

## Features

| Feature | Description |
|---|---|
| **Trade Feed** | Live stream of Kalshi trades, filtered by your min $ threshold |
| **Whale Detection** | Highlights trades above your whale $ threshold with blue border |
| **Unusual Flow Alerts** | Detects 75%+ one-sided volume clusters — possible insider positioning |
| **Hot Markets** | Sorted by volume, filterable by min market volume |
| **AI Analysis** | Claude analyzes your live feed for smart money patterns |
| **Auto Refresh** | Polls Kalshi every 10s / 30s / 1m / 2m automatically |
| **Demo Mode** | Toggle "Show mock data" to preview the UI without a server |

## Controls

- **Min trade $** — Filter out small trades from the feed
- **🐳 Whale $** — Threshold to flag a trade as a whale move
- **Min market vol $** — Minimum liquidity for a market to appear in Hot Markets
- **Category** — Filter the Hot Markets tab by topic
- **Whale only** — Hide non-whale trades from the feed
- **Detect unusual flow** — Run the one-sided clustering algorithm on each scan

## What to Watch For (Insider Signals)

1. **Concentrated YES/NO flow** — 3+ trades in the same market, 75%+ same side = alert
2. **Large trades in low-volume markets** — outsized position relative to liquidity
3. **Price movement with volume spike** — markets moving from 30¢→70¢ with volume
4. **New market early positioning** — big trades on freshly opened markets
5. **Cross-market correlation** — related markets (e.g. Fed cut + inflation) moving together

## API Endpoints (local proxy)

| Route | Description |
|---|---|
| `GET /api/trades` | Recent trades (proxied from Kalshi) |
| `GET /api/markets` | Open markets list |
| `GET /api/market/<ticker>` | Single market detail |
| `GET /api/orderbook/<ticker>` | Order book for a market |
| `GET /api/events` | Events with nested markets |
| `GET /api/health` | Check Kalshi connectivity |

## Notes

- Kalshi's public API does not require authentication for market data and trades
- All trade data is public — this does not access any private account information
- The AI Analysis feature uses Claude's API (no extra key needed when run via Claude.ai artifacts)
- Rate limit: Kalshi allows ~100 req/min on public endpoints
