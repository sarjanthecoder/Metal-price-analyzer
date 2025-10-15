import os
import requests
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import datetime
import random

# --- Configuration ---
# Get API key from environment variable (set in Render dashboard)
GOLD_API_KEY = os.environ.get('GOLD_API_KEY', 'goldapi-91a719mgrb30ey-io')
GOLD_API_URL = "https://www.goldapi.io/api/{symbol}/{currency}"

app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Supported metals with display names
METALS = {
    'XAU': 'Gold',
    'XAG': 'Silver',
    'XPT': 'Platinum',
    'XPD': 'Palladium',
    'XCU': 'Copper'
}

def fetch_metal_price(symbol="XAU", currency="USD"):
    """
    Fetches live metal price from GoldAPI.io.
    Returns price data or mock data if the API key is missing or an error occurs.
    """
    if not GOLD_API_KEY or GOLD_API_KEY == "your_api_key_here":
        print(f"WARNING: API key not found. Using mock data for {symbol}/{currency}.")
        return generate_mock_data(symbol, currency, error="API key not configured.")

    headers = {
        'x-access-token': GOLD_API_KEY,
        'Content-Type': 'application/json'
    }
    
    url = GOLD_API_URL.format(symbol=symbol, currency=currency)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check for API-side errors
        if 'error' in data:
            print(f"API returned an error for {symbol}/{currency}: {data['error']}")
            return generate_mock_data(symbol, currency, error=data['error'])

        return {
            "symbol": symbol,
            "name": METALS.get(symbol, symbol),
            "price": float(data.get('price', 0.0)),
            "prev_close_price": float(data.get('prev_close_price', 0.0)),
            "ch": float(data.get('ch', 0.0)),
            "change_pct": float(data.get('chp', 0.0)),
            "high": float(data.get('high_price', 0.0)),
            "low": float(data.get('low_price', 0.0)),
            "open": float(data.get('open_price', 0.0)),
            "currency": currency,
            "timestamp": data.get('timestamp', datetime.now().isoformat()),
            "status": "live_data",
            "data_source": "GoldAPI.io"
        }
        
    except requests.exceptions.RequestException as e:
        print(f"API Request Error for {symbol}/{currency}: {e}")
        return generate_mock_data(symbol, currency, error=str(e))
    except (ValueError, KeyError) as e:
        print(f"Data parsing error for {symbol}/{currency}: {e}")
        return generate_mock_data(symbol, currency, error=str(e))


def generate_mock_data(symbol, currency, error=None):
    """Generates realistic mock data for testing when the API is unavailable."""
    base_prices = {
        'XAU': 2350.0, 'XAG': 28.50, 'XPT': 1050.0, 
        'XPD': 1150.0, 'XCU': 4.25
    }
    base_price = base_prices.get(symbol, 1000.0)
    
    price_variation = random.uniform(-0.02, 0.02)
    current_price = base_price * (1 + price_variation)
    
    change_pct = random.uniform(-2.5, 2.5)
    prev_price = current_price / (1 + change_pct / 100)
    change_amount = current_price - prev_price
    
    high = current_price * random.uniform(1.005, 1.015)
    low = current_price * random.uniform(0.985, 0.995)
    
    return {
        "symbol": symbol, "name": METALS.get(symbol, symbol),
        "price": round(current_price, 2), "prev_close_price": round(prev_price, 2),
        "ch": round(change_amount, 2), "change_pct": round(change_pct, 2),
        "high": round(high, 2), "low": round(low, 2),
        "open": round(prev_price, 2), "currency": currency,
        "timestamp": datetime.now().isoformat(), "status": "mock_data",
        "data_source": "Mock Generator", "error": error
    }

# --- Flask Routes ---

@app.route('/')
def index():
    """Serve the main HTML page from the 'templates' folder."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

@app.route('/api/current-price', methods=['GET'])
def current_price():
    """API endpoint to get the current price for a specific metal."""
    symbol = request.args.get('symbol', 'XAU').upper()
    currency = request.args.get('currency', 'USD').upper()
    
    if symbol not in METALS:
        return jsonify({
            "error": f"Invalid symbol: {symbol}",
            "valid_symbols": list(METALS.keys())
        }), 400
    
    price_data = fetch_metal_price(symbol, currency)
    return jsonify(price_data)

@app.route('/api/metals', methods=['GET'])
def get_metals():
    """Get list of all supported metals"""
    return jsonify({
        "metals": METALS,
        "count": len(METALS)
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    # Use debug=False in production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)