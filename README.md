# Stroke Risk Prediction Project

## Overview
This project develops a machine learning-based web application to predict stroke risk using health and demographic data. It includes data preprocessing, model training, and a Flask-based web interface for user interaction. The application provides a user-friendly form to input personal and health information, predicts stroke risk, and displays results with visualizations.

## Project Structure
- **stroke_model.py**: Contains the data preprocessing, exploratory data analysis, model training, and model saving logic. It uses a Random Forest Classifier with hyperparameter tuning and SMOTE for handling imbalanced data.
- **app.py**: Flask backend that handles HTTP requests, serves the web interface, makes predictions using the trained model, and saves prediction reports in Excel files.
- **index.html**: Frontend HTML template with a multi-step form, Bootstrap styling, and JavaScript for form validation, AJAX requests, and result visualization (including a gauge for risk probability).
- **templates/**: Directory for HTML templates (contains index.html).
- **reports/**: Directory for storing daily prediction reports in Excel format.
- **stroke_prediction_model.pkl**: Saved Random Forest model (generated by stroke_model.py).
- **cleaned_stroke_data.csv**: Preprocessed dataset (generated by stroke_model.py).

## Features
- **Data Preprocessing**: Handles missing values, encodes categorical variables, and scales numerical features.
- **Exploratory Data Analysis**: Visualizations for stroke distribution, correlations, and feature relationships (e.g., age, BMI, glucose levels).
- **Machine Learning**: Trains multiple models (Logistic Regression, Random Forest, Decision Tree, SVM) and selects the best-performing Random Forest model with SMOTE and hyperparameter tuning.
- **Web Interface**: Multi-step form for user input, real-time validation, and a gauge-based result display with risk factors and recommendations.
- **Report Saving**: Saves predictions to daily Excel files and stores results locally in the browser.
- **API**: Provides a `/predict` endpoint for form-based predictions and an `/api/predict` endpoint for JSON-based predictions.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd stroke-prediction-project
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the `templates` and `reports` directories exist:
   ```bash
   mkdir templates reports
   ```
5. Place `index.html` in the `templates` directory and ensure `stroke_prediction_model.pkl` is in the project root.

## Usage
1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Open a browser and navigate to `http://127.0.0.1:5000`.
3. Complete the multi-step form with personal and health information.
4. Submit the form to receive a stroke risk prediction, displayed with a gauge and key risk factors.
5. Predictions are saved in the `reports` directory as daily Excel files.

## Dataset
The project uses the [Healthcare Dataset Stroke Data](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset) from Kaggle. The dataset includes features like age, gender, hypertension, heart disease, glucose levels, BMI, and smoking status, with a binary target variable for stroke occurrence.

## Model Details
- **Algorithm**: Random Forest Classifier
- **Preprocessing**: Median imputation for missing BMI, one-hot encoding for categorical variables, standard scaling for numerical features.
- **Handling Imbalance**: SMOTE oversampling and class weighting.
- **Hyperparameter Tuning**: Grid search over `n_estimators`, `max_depth`, `min_samples_split`, and `class_weight`.
- **Performance Metrics**: Evaluated using precision, recall, F1-score, and ROC-AUC.

## Dependencies
See `requirements.txt` for a complete list of Python packages. Key dependencies include:
- pandas
- numpy
- scikit-learn
- imblearn
- flask
- matplotlib
- seaborn
- joblib
- openpyxl

## Notes
- The model expects preprocessed data matching the training pipeline. For production, consider using the commented full pipeline in `stroke_model_notebook.ipynb` for raw data processing.
- The web interface uses Bootstrap, jQuery, and XLSX.js for frontend functionality.
- Prediction reports are stored in the `reports` directory with daily filenames (e.g., `stroke_predictions_20250511.xlsx`).
- The application includes error handling for invalid inputs and server errors.

## Future Improvements
- Implement a full preprocessing pipeline for raw data in production.
- Add user authentication for report access.
- Enhance visualizations with more interactive elements.
- Deploy the application to a cloud platform (e.g., Heroku, AWS).
- Add model retraining functionality for new data.

## License
This project is licensed under the MIT License.
