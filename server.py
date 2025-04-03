from flask import Flask
import threading
import time
from main import scrape_ipo_gmp  # Aapke scraping function ka import

app = Flask(__name__)

@app.route('/')
def home():
    return "Scraper API is Running!", 200

@app.route('/run_scraper')
def run_scraper():
    threading.Thread(target=scrape_ipo_gmp).start()
    return "Scraper started in the background!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
