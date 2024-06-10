from flask import Flask, render_template, jsonify
import numpy as np

app = Flask(__name__)

# Function to simulate stress scenarios (for Flask app)
def simulate_stress_scenarios_flask(days=30, scenarios=100):
    initial_price = 1800
    simulated_data = []
    for _ in range(scenarios):
        scenario = initial_price * (1 + np.random.normal(0, 0.05, days))
        simulated_data.append(scenario)
    return np.array(simulated_data)

# Function for stress testing (for Flask app)
def stress_test_flask(scenarios, initial_reserve, initial_coins):
    results = []
    for scenario in scenarios:
        final_gold_price = scenario[-1]
        reserve_value = initial_reserve * final_gold_price
        coins_required = reserve_value / 2  # 1:2 ratio
        coins_difference = coins_required - initial_coins
        results.append(coins_difference)
    return results

@app.route('/')
def index():
    # Run stress test for initial page load
    scenarios = simulate_stress_scenarios_flask()
    results = stress_test_flask(scenarios, 1000, 1000000)
    mean_adjustment = np.mean(results)
    std_adjustment = np.std(results)
    min_adjustment = np.min(results)
    max_adjustment = np.max(results)
    return render_template('index.html', mean_adjustment=mean_adjustment, std_adjustment=std_adjustment, min_adjustment=min_adjustment, max_adjustment=max_adjustment)

@app.route('/simulate')
def simulate():
    # Run a new stress test
    scenarios = simulate_stress_scenarios_flask()
    results = stress_test_flask(scenarios, 1000, 1000000)
    return jsonify(results.tolist())

if __name__ == '__main__':
    app.run(debug=True)