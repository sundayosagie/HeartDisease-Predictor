from flask import Flask, render_template, request
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the saved models and preprocessor
model = joblib.load("models/logistic_regression_model.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route for Predicting
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Extract features from form
        features = [
            float(request.form['Age']),
            float(request.form['RestingBP']),
            float(request.form['Cholesterol']),
            float(request.form['FastingBS']),
            float(request.form['MaxHR']),
            float(request.form['Oldpeak']),
            request.form['Sex'],
            request.form['ChestPainType'],
            request.form['RestingECG'],
            request.form['ExerciseAngina'],
            request.form['ST_Slope']
        ]

        # Convert to DataFrame
        input_data = {
            'Age': [features[0]],
            'RestingBP': [features[1]],
            'Cholesterol': [features[2]],
            'FastingBS': [features[3]],
            'MaxHR': [features[4]],
            'Oldpeak': [features[5]],
            'Sex': [features[6]],
            'ChestPainType': [features[7]],
            'RestingECG': [features[8]],
            'ExerciseAngina': [features[9]],
            'ST_Slope': [features[10]]
        }

        import pandas as pd
        df_input = pd.DataFrame(input_data)

        # Transform using preprocessor
        transformed_input = preprocessor.transform(df_input)

        # Make prediction
        prediction = model.predict(transformed_input)[0]
        result = "Positive for Heart Disease" if prediction == 1 else "No Heart Disease Detected"

        return render_template('result.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)