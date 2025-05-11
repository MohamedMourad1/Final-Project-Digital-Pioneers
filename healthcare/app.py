from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import joblib
import os
import openpyxl
from datetime import datetime

app = Flask(__name__)

# Load the trained model
model = joblib.load('stroke_prediction_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Create a DataFrame with the input features
        # These should match the features used during training (after preprocessing)
        features = {
            'age': float(data['age']),
            'hypertension': int(data['hypertension']),
            'heart_disease': int(data['heart_disease']),
            'avg_glucose_level': float(data['avg_glucose_level']),
            'bmi': float(data['bmi'])
        }
        
        # Add one-hot encoded categorical features
        # Gender
        features['gender_Male'] = 1 if data['gender'] == 'Male' else 0
        features['gender_Other'] = 1 if data['gender'] == 'Other' else 0
        
        # Ever married
        features['ever_married_Yes'] = 1 if data['ever_married'] == 'Yes' else 0
        
        # Work type
        features['work_type_Never_worked'] = 1 if data['work_type'] == 'Never_worked' else 0
        features['work_type_Private'] = 1 if data['work_type'] == 'Private' else 0
        features['work_type_Self-employed'] = 1 if data['work_type'] == 'Self-employed' else 0
        features['work_type_children'] = 1 if data['work_type'] == 'children' else 0
        
        # Residence type
        features['Residence_type_Urban'] = 1 if data['Residence_type'] == 'Urban' else 0
        
        # Smoking status
        features['smoking_status_formerly smoked'] = 1 if data['smoking_status'] == 'formerly smoked' else 0
        features['smoking_status_never smoked'] = 1 if data['smoking_status'] == 'never smoked' else 0
        features['smoking_status_smokes'] = 1 if data['smoking_status'] == 'smokes' else 0
        
        # Convert to DataFrame
        input_df = pd.DataFrame([features])
        
        # Make prediction
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)[:, 1][0]
        
        # Return result
        result = {
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'message': 'High risk of stroke' if prediction[0] == 1 else 'Low risk of stroke'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        # Get JSON data
        data = request.get_json()
        
        # Create a DataFrame with the input features
        features = {
            'age': float(data['age']),
            'hypertension': int(data['hypertension']),
            'heart_disease': int(data['heart_disease']),
            'avg_glucose_level': float(data['avg_glucose_level']),
            'bmi': float(data['bmi'])
        }
        
        # Add one-hot encoded categorical features
        # Gender
        features['gender_Male'] = 1 if data['gender'] == 'Male' else 0
        features['gender_Other'] = 1 if data['gender'] == 'Other' else 0
        
        # Ever married
        features['ever_married_Yes'] = 1 if data['ever_married'] == 'Yes' else 0
        
        # Work type
        features['work_type_Never_worked'] = 1 if data['work_type'] == 'Never_worked' else 0
        features['work_type_Private'] = 1 if data['work_type'] == 'Private' else 0
        features['work_type_Self-employed'] = 1 if data['work_type'] == 'Self-employed' else 0
        features['work_type_children'] = 1 if data['work_type'] == 'children' else 0
        
        # Residence type
        features['Residence_type_Urban'] = 1 if data['Residence_type'] == 'Urban' else 0
        
        # Smoking status
        features['smoking_status_formerly smoked'] = 1 if data['smoking_status'] == 'formerly smoked' else 0
        features['smoking_status_never smoked'] = 1 if data['smoking_status'] == 'never smoked' else 0
        features['smoking_status_smokes'] = 1 if data['smoking_status'] == 'smokes' else 0
        
        # Convert to DataFrame
        input_df = pd.DataFrame([features])
        
        # Make prediction
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)[:, 1][0]
        
        # Return result
        result = {
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'message': 'High risk of stroke' if prediction[0] == 1 else 'Low risk of stroke'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/save-report', methods=['POST'])
def save_report():
    try:
        # Get JSON data
        result = request.get_json()
        
        # Define Excel file path (daily file)
        filename = os.path.join('reports', f"stroke_predictions_{datetime.now().strftime('%Y%m%d')}.xlsx")
        
        # Define headers for Excel file
        headers = [
            "Username", "Timestamp", "Age", "Gender", "Ever Married", "Residence Type",
            "Work Type", "Hypertension", "Heart Disease", "Avg Glucose Level", "BMI",
            "Smoking Status", "Risk Probability (%)", "Risk Level"
        ]
        
        # Prepare data row
        data_row = [
            result.get('username', ''),
            result.get('timestamp', ''),
            result.get('age', ''),
            result.get('gender', ''),
            result.get('ever_married', ''),
            result.get('residence_type', ''),
            result.get('work_type', ''),
            result.get('hypertension', ''),
            result.get('heart_disease', ''),
            result.get('avg_glucose_level', ''),
            result.get('bmi', ''),
            result.get('smoking_status', ''),
            result.get('probability', ''),
            result.get('risk_level', '')
        ]
        
        # Load or create Excel file
        if os.path.exists(filename):
            workbook = openpyxl.load_workbook(filename)
            worksheet = workbook.active
        else:
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.append(headers)  # Add headers if new file
        
        # Append data row
        worksheet.append(data_row)
        
        # Save Excel file
        workbook.save(filename)
        
        return jsonify({'status': 'success', 'message': 'Report saved'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create reports directory if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    app.run(debug=True)

