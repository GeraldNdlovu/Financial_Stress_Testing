from flask import Flask, render_template, jsonify
import numpy as np
import pandas_datareader.data as web
import datetime

app = Flask(__name__)

# Fetch historical gold price data
def fetch_gold_data():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.today()
    gold_data = web.DataReader('GOLDAMGBD228NLBM', 'fred', start, end)
    gold_data.dropna(inplace=True)
    gold_data['Returns'] = gold_data['GOLDAMGBD228NLBM'].pct_change().dropna()
    return gold_data

# Function to simulate GBM paths
def simulate_gbm(s0, mu, sigma, T, dt=1/252, n_scenarios=1000):
    n_steps = int(T / dt)
    paths = np.zeros((n_steps, n_scenarios))
    paths[0] = s0
    
    for t in range(1, n_steps):
        z = np.random.standard_normal(n_scenarios)
        paths[t] = paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    return paths

# Function for stress testing
def stress_test_gbm(simulated_paths, initial_reserve, initial_coins):
    results = []
    for path in simulated_paths.T:
        final_gold_price = path[-1]
        reserve_value = initial_reserve * final_gold_price
        coins_required = reserve_value / 2
        coins_difference = coins_required - initial_coins
        results.append(coins_difference)
    return results

@app.route('/')
def index():
    gold_data = fetch_gold_data()
    s0 = gold_data['GOLDAMGBD228NLBM'].iloc[-1]
    mu = gold_data['Returns'].mean()
    sigma = gold_data['Returns'].std()
    T = 1
    
    simulated_paths = simulate_gbm(s0, mu, sigma, T)
    results = stress_test_gbm(simulated_paths, 1000, 1000000)
    
    mean_adjustment = np.mean(results)
    std_adjustment = np.std(results)
    min_adjustment = np.min(results)
    max_adjustment = np.max(results)
    
    return render_template('index.html', mean_adjustment=mean_adjustment, std_adjustment=std_adjustment, min_adjustment=min_adjustment, max_adjustment=max_adjustment)

@app.route('/simulate')
def simulate():
    gold_data = fetch_gold_data()
    s0 = gold_data['GOLDAMGBD228NLBM'].iloc[-1]
    mu = gold_data['Returns'].mean()
    sigma = gold_data['Returns'].std()
    T = 1
    
    simulated_paths = simulate_gbm(s0, mu, sigma, T)
    results = stress_test_gbm(simulated_paths, 1000, 1000000)
    
    return jsonify(results.tolist())

if __name__ == '__main__':
    app.run(debug=True)
