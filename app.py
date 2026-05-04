from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Thrissur Gold API - Live"

@app.route('/api/gold/thrissur')
def get_gold():
    try:
        # Method 1: GoldAPI - India rate. Thrissur-ന് +₹15 add ചെയ്യുന്നു
        url = "https://api.gold-api.com/price/XAU"
        headers = {'X-API-KEY': 'goldapi-demo'}  # Free demo key
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            # 1 ounce = 31.1035 grams. 1 USD = 83.5 INR approx
            price_per_gram_24k = data['price'] / 31.1035 * 83.5
            price_22k_1g = price_per_gram_24k * 0.916 + 15  # Thrissur premium
            price_24k_1g = price_per_gram_24k + 15
            price_22k_8g = price_22k_1g * 8
            
            return jsonify({
                "city": "Thrissur",
                "source": "GoldAPI Live",
                "24_carat_1g": f"₹{price_24k_1g:.0f}",
                "22_carat_1g": f"₹{price_22k_1g:.0f}",
                "22_carat_8g": f"₹{price_22k_8g:.0f}",
                "status": "live",
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            raise Exception("GoldAPI failed")
            
    except Exception as e:
        # Method 2: Fallback - Manual rate. ഇത് ദിവസം 1 തവണ update ചെയ്യണം
        return jsonify({
            "city": "Thrissur",
            "source": "Manual",
            "24_carat_1g": "₹9,970",
            "22_carat_1g": "₹9,140", 
            "22_carat_8g": "₹73,120",
            "status": "manual",
            "note": "Update manually in code",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

if __name__ == '__main__':
    app.run()
