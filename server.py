"""
KalshiPulse - Proxy Server for Render.com deployment
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
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/trades")
def trades():
    try:
        params = {"limit": request.args.get("limit", 200)}
        ticker = request.args.get("ticker")
        if ticker:
            params["ticker"] = ticker
        data = kalshi_get("/trades", params=params)
        return jsonify(data)
    except requests.HTTPError as e:
        return jsonify({"error": f"Kalshi API error: {e.response.status_code} - {e.response.text}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/markets")
def markets():
    try:
        params = {
            "status": request.args.get("status", "open"),
            "limit": request.args.get("limit", 200),
        }
        data = kalshi_get("/markets", params=params)
        return jsonify(data)
    except requests.HTTPError as e:
        return jsonify({"error": f"Kalshi API error: {e.response.status_code} - {e.response.text}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/market/<ticker>")
def market_detail(ticker):
    try:
        data = kalshi_get(f"/markets/{ticker}")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/orderbook/<ticker>")
def orderbook(ticker):
    try:
        data = kalshi_get(f"/markets/{ticker}/orderbook")
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
        kalshi_get("/markets?limit=1&status=open")
        return jsonify({"status": "ok", "kalshi": "reachable"})
    except Exception as e:
        return jsonify({"status": "degraded", "error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
