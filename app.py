from flask import Flask, render_template
import pandas_datareader.data as web
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    start = datetime(2023, 9, 23)
    end = datetime(2023, 10, 23)
    df = web.DataReader('AAPL', 'yahoo', start, end)
    return render_template('index.html', data=df.to_html())

if __name__ == '__main__':
    app.run(debug=True)

