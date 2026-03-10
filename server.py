"""
KalshiPulse - Local Proxy Server
Proxies requests to Kalshi's public API to avoid CORS issues in the browser.
Run: python server.py
Then open: http://localhost:5000
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder=".")
CORS(app)

KALSHI_BASE = "https://api.elections.kalshi.com/trade-api/v2"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "KalshiPulse/1.0",
}


def kalshi_get(path, params=None):
    url = f"{KALSHI_BASE}{path}"
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/trades")
def trades():
    try:
        limit = request.args.get("limit", 200)
        ticker = request.args.get("ticker", None)
        params = {"limit": limit}
        if ticker:
            params["ticker"] = ticker
        data = kalshi_get("/trades", params=params)
        return jsonify(data)
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "status": e.response.status_code}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/markets")
def markets():
    try:
        params = {
            "status": request.args.get("status", "open"),
            "limit": request.args.get("limit", 200),
        }
        series_ticker = request.args.get("series_ticker")
        if series_ticker:
            params["series_ticker"] = series_ticker
        data = kalshi_get("/markets", params=params)
        return jsonify(data)
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "status": e.response.status_code}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/market/<ticker>")
def market_detail(ticker):
    try:
        data = kalshi_get(f"/markets/{ticker}")
        return jsonify(data)
    except requests.HTTPError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/orderbook/<ticker>")
def orderbook(ticker):
    try:
        data = kalshi_get(f"/markets/{ticker}/orderbook")
        return jsonify(data)
    except requests.HTTPError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/series")
def series():
    try:
        params = {"limit": request.args.get("limit", 100)}
        data = kalshi_get("/series", params=params)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/events")
def events():
    try:
        params = {
            "status": request.args.get("status", "open"),
            "limit": request.args.get("limit", 100),
            "with_nested_markets": "true",
        }
        data = kalshi_get("/events", params=params)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health")
def health():
    try:
        kalshi_get("/exchange/status")
        return jsonify({"status": "ok", "kalshi": "reachable"})
    except Exception as e:
        return jsonify({"status": "degraded", "error": str(e)}), 200


if __name__ == "__main__":
    print("\n🚀 KalshiPulse server starting...")
    print("📡 Proxying: https://api.elections.kalshi.com/trade-api/v2")
    print("🌐 Open your browser at: http://localhost:5000\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

