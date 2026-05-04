from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Thrissur Gold API - Live"

@app.route('/api/gold/thrissur')
def get_gold():
    try:
        url = "https://www.goodreturns.in/gold-rates/thrissur.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        # GoodReturns-ന്റെ structure stable ആണ്
        table = soup.find('table', class_='gold_silver_table')
        rows = table.find_all('tr')

        gold_22k = ""
        gold_24k = ""

        for row in rows:
            if '22 Carat' in row.text:
                gold_22k = row.find_all('td')[1].text.strip()
            if '24 Carat' in row.text:
                gold_24k = row.find_all('td')[1].text.strip()

        if not gold_22k:
            raise Exception("Rate not found")

        gold_22k_8g = float(gold_22k.replace('₹','').replace(',','')) * 8

        return jsonify({
            "city": "Thrissur",
            "source": "GoodReturns",
            "24_carat_1g": gold_24k,
            "22_carat_1g": gold_22k,
            "22_carat_8g": f"₹{gold_22k_8g:.0f}",
            "status": "live",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        return jsonify({
            "city": "Thrissur",
            "source": "Cached",
            "24_carat_1g": "₹9,955",
            "22_carat_1g": "₹9,125",
            "22_carat_8g": "₹73,000",
            "status": "cached",
            "error": str(e),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

if __name__ == '__main__':
    app.run()
