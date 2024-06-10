from flask import Flask, render_template, jsonify
from services.data_acquisition_service import collect_data
from services.model_training_service import train_models
from services.prediction_service import predict_impact
from services.analysis_service import analyze_predictions
from services.user_interaction_service import display_results

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect-data')
def collect_data_route():
    historical_gold_price_data = collect_data()
    return jsonify(historical_gold_price_data)

@app.route('/train-models')
def train_models_route():
    historical_gold_price_data = collect_data_route()
    machine_learning_model = train_models(historical_gold_price_data)
    return jsonify(machine_learning_model)

@app.route('/predict-impact')
def predict_impact_route():
    machine_learning_model = train_models_route()
    stress_test_prediction = predict_impact(machine_learning_model)
    return jsonify(stress_test_prediction)

@app.route('/analyze-predictions')
def analyze_predictions_route():
    stress_test_prediction = predict_impact_route()
    stress_test_report = analyze_predictions(stress_test_prediction)
    return jsonify(stress_test_report)

@app.route('/display-results')
def display_results_route():
    stress_test_report = analyze_predictions_route()
    return display_results(stress_test_report)

if __name__ == '__main__':
    app.run(debug=True)
