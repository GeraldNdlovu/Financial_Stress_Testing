from sklearn.model_selection import train_test_split
import os
import pandas as pd
from flask import Flask, render_template, request
import kaggle

app = Flask(__name__)

def download_kaggle_dataset():
    kaggle.api.authenticate()
    dataset_path = 'data/monthly_csv.csv'
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.isfile(dataset_path):
        kaggle.api.dataset_download_files('nhiyen/monthly-gold-price', path='data/', unzip=True)

def load_and_preprocess_data():
    download_kaggle_dataset()
    gold_data = pd.read_csv('data/monthly_csv.csv')
    gold_data['Date'] = pd.to_datetime(gold_data['Date'])
    gold_data.set_index('Date', inplace=True)
    gold_data['Daily_Return'] = gold_data['Price'].pct_change()
    gold_data.dropna(inplace=True)
    gold_data['Volatility'] = gold_data['Daily_Return'].rolling(window=30).std()
    return gold_data

def train_model(gold_data):
    X = gold_data[['Volatility']]
    y = gold_data['Price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model, X_test, y_test

def plot_predictions(model, X_test, y_test):
    predictions = model.predict(X_test)
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.index, y_test.values, label='Actual Price', color='blue')
    plt.plot(y_test.index, predictions, label='Predicted Price', color='red')
    plt.xlabel('Date')
    plt.ylabel('Gold Price')
    plt.title('Actual vs. Predicted Gold Prices')
    plt.legend()
    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    return plot_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gold_data = load_and_preprocess_data()
        model, X_test, y_test = train_model(gold_data)
        plot_path = plot_predictions(model, X_test, y_test)
        return render_template('index.html', plot_url=plot_path)
    return render_template('index.html', plot_url=None)

if __name__ == '__main__':
    app.run(debug=True)
