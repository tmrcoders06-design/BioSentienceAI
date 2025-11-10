"""
BioSentience Web Application
=============================
Flask-based biological data analysis platform with ML predictions,
explainability, and interactive simulations.
"""

from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import numpy as np
import joblib
import json
import os
from werkzeug.utils import secure_filename
import traceback

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create uploads directory
os.makedirs('uploads', exist_ok=True)

# Load trained models and metadata
print("Loading ML models...")
models = {
    'health_index': joblib.load('models/health_index_model.pkl'),
    'mutation_risk': joblib.load('models/mutation_risk_model.pkl'),
    'adaptation_score': joblib.load('models/adaptation_score_model.pkl')
}

with open('models/metadata.json', 'r') as f:
    metadata = json.load(f)

feature_names = metadata['features']
print(f"Models loaded. Features: {feature_names}")

# Expected feature names
EXPECTED_FEATURES = feature_names

def validate_and_prepare_data(df):
    """Validate uploaded data and prepare for prediction"""
    # Check if all required features are present
    missing_features = set(EXPECTED_FEATURES) - set(df.columns)
    if missing_features:
        return None, f"Missing required features: {', '.join(missing_features)}"
    
    # Select and order features correctly
    X = df[EXPECTED_FEATURES]
    
    # Check for missing values
    if X.isnull().any().any():
        return None, "Data contains missing values. Please ensure all fields are filled."
    
    # Validate data ranges (biological constraints)
    if (X < 0).any().any():
        return None, "Data contains negative values. Biological metrics must be non-negative."
    
    return X, None

def generate_explanation(feature_values, predictions, feature_importances):
    """Generate natural language explanation for predictions"""
    explanation = {
        'health_index': [],
        'mutation_risk': [],
        'adaptation_score': [],
        'summary': ''
    }
    
    # Get feature contributions for this prediction
    for target in ['health_index', 'mutation_risk', 'adaptation_score']:
        importances = metadata['models'][target]['top_features']
        
        for feat_info in importances[:3]:  # Top 3 features
            feat_name = feat_info['name']
            importance = feat_info['importance']
            value = feature_values[feat_name].values[0]
            
            # Convert feature names to readable format
            readable_name = feat_name.replace('_', ' ').title()
            
            explanation[target].append({
                'feature': readable_name,
                'value': float(value),
                'importance': float(importance),
                'impact': 'high' if importance > 0.15 else 'moderate' if importance > 0.08 else 'low'
            })
    
    # Generate summary
    health = predictions['health_index']
    risk = predictions['mutation_risk']
    adaptation = predictions['adaptation_score']
    
    health_status = 'excellent' if health > 0.85 else 'good' if health > 0.70 else 'moderate' if health > 0.55 else 'concerning'
    risk_status = 'low' if risk < 0.15 else 'moderate' if risk < 0.30 else 'elevated' if risk < 0.45 else 'high'
    adaptation_status = 'high' if adaptation > 0.80 else 'moderate' if adaptation > 0.60 else 'low'
    
    explanation['summary'] = (
        f"The biological system shows {health_status} health (index: {health:.2f}) "
        f"with {risk_status} mutation risk ({risk:.2f}) and {adaptation_status} "
        f"adaptation capability ({adaptation:.2f}). "
    )
    
    # Add key drivers
    top_health_feature = explanation['health_index'][0]['feature']
    top_risk_feature = explanation['mutation_risk'][0]['feature']
    
    explanation['summary'] += (
        f"Primary health driver: {top_health_feature}. "
        f"Main risk factor: {top_risk_feature}."
    )
    
    return explanation

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload and return preview"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are supported'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read and validate
        df = pd.read_csv(filepath)
        
        # Store filepath in session
        session['current_file'] = filepath
        
        # Return preview
        preview = {
            'filename': filename,
            'rows': len(df),
            'columns': list(df.columns),
            'preview_data': df.head(10).to_dict(orient='records'),
            'has_required_features': all(feat in df.columns for feat in EXPECTED_FEATURES)
        }
        
        return jsonify(preview)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded data and return predictions with explanations"""
    try:
        data = request.json
        
        # Handle both file upload and direct data input
        if 'data' in data:
            # Direct data input
            df = pd.DataFrame([data['data']])
        elif 'current_file' in session:
            # Use uploaded file
            filepath = session['current_file']
            df = pd.read_csv(filepath)
            
            # If row_index specified, analyze that row
            if 'row_index' in data:
                row_idx = data['row_index']
                df = df.iloc[[row_idx]]
        else:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate and prepare data
        X, error = validate_and_prepare_data(df)
        if error:
            return jsonify({'error': error}), 400
        
        # Make predictions
        predictions = {}
        confidence_scores = {}
        
        for target_name, model in models.items():
            pred = model.predict(X)[0]
            predictions[target_name] = float(pred)
            
            # Calculate confidence based on model performance
            r2 = metadata['models'][target_name]['r2_score']
            confidence_scores[target_name] = float(r2)
        
        # Generate explanations
        explanation = generate_explanation(X, predictions, models)
        
        # Prepare response
        response = {
            'predictions': predictions,
            'confidence': confidence_scores,
            'explanation': explanation,
            'input_features': X.iloc[0].to_dict(),
            'disclaimer': 'These are model predictions for research purposes only. Not medical advice.'
        }
        
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Run simulation by varying a parameter and projecting trajectory"""
    try:
        data = request.json
        base_features = data.get('base_features')
        vary_feature = data.get('vary_feature')
        steps = data.get('steps', 10)
        variation_range = data.get('variation_range', 0.3)  # ±30% by default
        
        if not base_features or not vary_feature:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Create base dataframe
        df_base = pd.DataFrame([base_features])
        
        # Validate base features
        X_base, error = validate_and_prepare_data(df_base)
        if error:
            return jsonify({'error': error}), 400
        
        # Get base value
        base_value = base_features[vary_feature]
        
        # Create simulation trajectory
        trajectory = []
        
        for i in range(steps):
            # Vary the feature
            factor = 1 - variation_range + (2 * variation_range * i / (steps - 1))
            new_value = base_value * factor
            
            # Create modified features
            modified_features = base_features.copy()
            modified_features[vary_feature] = new_value
            
            df_sim = pd.DataFrame([modified_features])
            X_sim, _ = validate_and_prepare_data(df_sim)
            
            # Predict with all models
            step_predictions = {
                'step': i,
                vary_feature: float(new_value)
            }
            
            for target_name, model in models.items():
                pred = model.predict(X_sim)[0]
                step_predictions[target_name] = float(pred)
            
            trajectory.append(step_predictions)
        
        response = {
            'trajectory': trajectory,
            'varied_feature': vary_feature,
            'base_value': float(base_value),
            'variation_range': variation_range,
            'steps': steps
        }
        
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Simulation error: {str(e)}'}), 500

@app.route('/api/explain', methods=['POST'])
def explain():
    """Get detailed feature importance explanation for a specific prediction"""
    try:
        data = request.json
        target = data.get('target', 'health_index')
        
        if target not in models:
            return jsonify({'error': f'Invalid target: {target}'}), 400
        
        model_info = metadata['models'][target]
        
        explanation = {
            'target': target,
            'description': model_info['description'],
            'performance': {
                'r2_score': model_info['r2_score'],
                'mse': model_info['mse']
            },
            'feature_importances': model_info['top_features'],
            'interpretation': f"This model predicts {model_info['description']} with {model_info['r2_score']:.1%} accuracy."
        }
        
        return jsonify(explanation)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Explanation error: {str(e)}'}), 500

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Return sample data for demo purposes"""
    df = pd.read_csv('data/sample_biological_data.csv')
    sample = df[EXPECTED_FEATURES].iloc[0].to_dict()
    return jsonify({
        'data': sample,
        'note': 'This is demo data from the training dataset'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
