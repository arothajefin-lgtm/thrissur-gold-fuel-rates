from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Thrissur Gold API - Debug Mode"

@app.route('/api/gold/thrissur')
def get_gold():
    try:
        url = "https://www.ndtv.com/gold-rate/gold-price-thrissur"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=20)
        
        # Debug: എന്താ കിട്ടിയത് എന്ന് log ചെയ്യുക
        print(f"NDTV Status Code: {r.status_code}")
        print(f"NDTV HTML Length: {len(r.text)}")
        print(f"NDTV HTML Start: {r.text[:500]}")  # ആദ്യ 500 character
        
        if r.status_code != 200:
            raise Exception(f"NDTV returned {r.status_code}")
        
        if "22 Carat" not in r.text and "gold22k" not in r.text:
            raise Exception("NDTV page changed - rate keywords not found")
        
        # ഇവിടെ നിന്റെ പഴയ parsing code ഇടാം
        return jsonify({
            "status": "debug",
            "ndtv_status": r.status_code,
            "html_length": len(r.text),
            "message": "Check Render logs for HTML start"
        })
            
    except Exception as e:
        return jsonify({
            "city": "Thrissur",
            "source": "Manual",
            "24_carat_1g": "₹13,858",
            "22_carat_1g": "₹12,703",
            "22_carat_8g": "₹1,01,624",
            "status": "manual",
            "error": str(e),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

if __name__ == '__main__':
    app.run()
