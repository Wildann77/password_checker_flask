import os
from flask import Flask, request, jsonify, render_template
import joblib
from utils.features import extract_features

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

model_path = os.path.join(BASE_DIR, 'model', 'manual_password_model300.pkl')
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('index.html')  # index.html harus ada di /templates

@app.route('/predict', methods=['POST'])
def predict():
    password = request.form.get('password') or request.json.get('password')
    if not password:
        return jsonify({'error': 'Password required'}), 400

    features = extract_features(password)
    strength = model.predict(features)[0]

    if request.form:
        return render_template("index.html", result=strength, password=password)

    return jsonify({'strength': strength})

if __name__ == '__main__':
    app.run(debug=True)
