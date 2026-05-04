from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "Thrissur Gold API - The Hindu BusinessLine"

@app.route('/api/gold/thrissur')
def get_gold():
    try:
        url = "https://www.thehindubusinessline.com/gold-rate-today/Thrissur/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Method 1: table തിരയുക
        gold_24k = ""
        gold_22k = ""

        # എല്ലാ table-ഉം check ചെയ്യുക
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                text = row.get_text()
                if '24 Carat' in text or '24 Karat' in text:
                    # ₹9,955 പോലെ price extract ചെയ്യുക
                    price = re.findall(r'₹[\d,]+', text)
                    if price:
                        gold_24k = price[0].replace(',', '')
                if '22 Carat' in text or '22 Karat' in text:
                    price = re.findall(r'₹[\d,]+', text)
                    if price:
                        gold_22k = price[0].replace(',', '')

        # Method 2: Direct text search - table കിട്ടിയില്ലെങ്കിൽ
        if not gold_22k:
            page_text = soup.get_text()
            # "22 Carat ₹9,125" pattern തിരയുക
            match_22k = re.search(r'22\s*Carat\s*₹([\d,]+)', page_text, re.IGNORECASE)
            match_24k = re.search(r'24\s*Carat\s*₹([\d,]+)', page_text, re.IGNORECASE)
            if match_22k:
                gold_22k = f"₹{match_22k.group(1)}"
            if match_24k:
                gold_24k = f"₹{match_24k.group(1)}"

        if not gold_22k or not gold_24k:
            raise Exception("Could not parse gold rates from page")

        # 8 gram calculate ചെയ്യുക
        gold_22k_8g = float(gold_22k.replace('₹','').replace(',','')) * 8

        return jsonify({
            "city": "Thrissur",
            "source": "The Hindu BusinessLine",
            "24_carat_1g": gold_24k,
            "22_carat_1g": gold_22k,
            "22_carat_8g": f"₹{gold_22k_8g:.0f}",
            "status": "live",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        # Scrape പൊട്ടിയാൽ ഇപ്പോഴത്തെ approximate rate
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
