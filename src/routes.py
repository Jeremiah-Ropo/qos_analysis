import os
import pickle
from flask import request, jsonify
import pyrebase
# from src.config import firebase_config
import pandas as pd
from src.pipelines import feature_engineering, process_testing_dataset, save_predicted_values
from src.notification import get_random_notification


# # Initialize Firebase
# firebase = pyrebase.initialize_app(firebase_config)
# db = firebase.database()

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'final_model.pkl')
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# # Add data to Firebase
# def add_data():
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
    
#     # Add data to Firebase
#     db.child("users").push(data)
#     return jsonify({"status": "success", "data": data}), 201

# # Retrieve data from Firebase
# def get_data():
#     all_data = db.child("users").get()
#     print(all_data)
#     data_list = all_data.val() if all_data.val() else []
#     return jsonify({"status": "success", "data": data_list}), 200

# Predict endpoint
def predict():
    try:
        # Get input data from the request
        data = request.get_json()

        # Ensure required fields are present
        required_fields = [
            'Device Id', 'Date', 'Time', 'Download', 'Upload', 'Latency',
            'DNS Lookup', 'RSS', 'Device Model', 'Device Brand Name', 
            'Manufacture', 'OS Version', 'OS Core', 'Battery Charge Level', 
            'Operator Name', 'Network Type', 'Longitude', 'Latitude', 
            'State', 'Country'
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        # Convert data to a DataFrame with one row
        input_data = pd.DataFrame([data])

        # Apply feature engineering
        input_data = feature_engineering(input_data)

        # Process the testing dataset
        input_data = process_testing_dataset(input_data)

        # Ensure model/scaler expects DataFrame with valid feature names
        if hasattr(model, 'feature_names_in_'):
            missing_features = set(model.feature_names_in_) - set(input_data.columns)
            if missing_features:
                return jsonify({'error': f'Missing features: {missing_features}'}), 400

        # Convert DataFrame to NumPy array
        input_array = input_data.to_numpy()

        # Predict using the loaded model
        prediction = model.predict(input_array)[0]

        # Save the predicted values
        input_data = save_predicted_values(input_data, prediction)

        # Determine the QoS category
        if prediction == 0:
            qos_category = 'below_average'
        elif prediction == 1:
            qos_category = 'above_average'
        else:
            qos_category = 'average'

        # Generate notification message
        notification_message = get_random_notification(qos_category)

        # Return the prediction result
        return jsonify({
            'status': 'success',
            'prediction': int(prediction),
            'notification': notification_message
        }), 200

    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'message': str(e)}), 500
