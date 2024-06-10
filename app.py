from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Placeholder data for demonstration purposes
    model_data = {
        'scenario': 'Sudden Increase in Gold Price',
        'new_gold_price': '$2500 per ounce',
        'reserve_value': '$2,500,000',
        'coins_required_to_maintain_peg': '1,250,000 coins',
        'coins_to_mint': '250,000 coins'
    }
    return render_template('index.html', data=model_data)

if __name__ == '__main__':
    app.run(debug=True)
