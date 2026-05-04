from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "Thrissur Gold API - NDTV"

@app.route('/api/gold/thrissur')
def get_gold():
    try:
        url = "https://www.ndtv.com/gold-rate/gold-price-thrissur"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        # NDTV-ൽ rate direct text ആയിട്ടുണ്ട്
        text = soup.get_text()
        
        # "22 Carat Gold : ₹ 12703" pattern
        match_22k = re.search(r'22\s*Carat\s*Gold\s*:?\s*₹\s*([\d,]+)', text, re.IGNORECASE)
        match_24k = re.search(r'24\s*Carat\s*Gold\s*:?\s*₹\s*([\d,]+)', text, re.IGNORECASE)
        
        if not match_22k or not match_24k:
            raise Exception("Rate not found on NDTV page")

        gold_22k_1g = float(match_22k.group(1).replace(',', ''))
        gold_24k_1g = float(match_24k.group(1).replace(',', ''))
        gold_22k_8g = gold_22k_1g * 8

        return jsonify({
            "city": "Thrissur",
            "source": "NDTV",
            "24_carat_1g": f"₹{gold_24k_1g:.0f}",
            "22_carat_1g": f"₹{gold_22k_1g:.0f}",
            "22_carat_8g": f"₹{gold_22k_8g:.0f}",
            "status": "live",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
