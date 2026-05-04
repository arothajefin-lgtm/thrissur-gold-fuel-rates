from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Thrissur Gold API - The Hindu BusinessLine"

@app.route('/api/gold/thrissur')
def get_gold():
    try:
        url = "https://www.thehindubusinessline.com/gold-rate-today/Thrissur/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        # The Hindu BusinessLine-ന്റെ table structure
        table = soup.find('table', class_='bl-table')
        rows = table.find_all('tr')

        gold_24k = ""
        gold_22k = ""

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                if '24 Carat' in cols[0].text:
                    gold_24k = cols[1].text.strip().replace(',', '')
                if '22 Carat' in cols[0].text:
                    gold_22k = cols[1].text.strip().replace(',', '')

        # 8 gram calculate ചെയ്യുക
        gold_22k_8g = float(gold_22k.replace('₹','')) * 8

        return jsonify({
            "city": "Thrissur",
            "source": "The Hindu BusinessLine",
            "24_carat_1g": gold_24k,
            "22_carat_1g": f"₹{gold_22k}",
            "22_carat_8g": f"₹{gold_22k_8g:.0f}",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        # Site scrape പൊട്ടിയാൽ fallback values
        return jsonify({
            "city": "Thrissur",
            "source": "Cached",
            "24_carat_1g": "₹9,955",
            "22_carat_1g": "₹9,125",
            "22_carat_8g": "₹73,000",
            "error": str(e),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

if __name__ == '__main__':
    app.run()
