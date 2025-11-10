"""
BioSentience Model Training Pipeline
=====================================
This script trains Random Forest models on biological data to predict:
1. Health Index (0-1 scale)
2. Mutation Risk (0-1 scale)
3. Adaptation Score (0-1 scale)

Dataset: Sample biological measurements including gene expression levels,
cell metrics, and environmental variables.

Model Type: Random Forest Regressor (scikit-learn)
Output: Saved models in models/ directory with feature names and metadata
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
from datetime import datetime

print("=" * 60)
print("BioSentience ML Training Pipeline")
print("=" * 60)

# Load the biological dataset
print("\n[1/6] Loading biological dataset...")
df = pd.read_csv('data/sample_biological_data.csv')
print(f"   Loaded {len(df)} samples with {len(df.columns)} features")
print(f"   Features: {', '.join(df.columns[:5])}... (and {len(df.columns)-5} more)")

# Define feature columns (all except the three target variables)
feature_cols = [col for col in df.columns if col not in ['health_index', 'mutation_risk', 'adaptation_score']]
X = df[feature_cols]
print(f"\n   Using {len(feature_cols)} input features for prediction")

# Define targets
targets = {
    'health_index': 'Health Index (overall biological wellness)',
    'mutation_risk': 'Mutation Risk (genetic instability probability)',
    'adaptation_score': 'Adaptation Score (environmental resilience)'
}

# Train a model for each target
models = {}
metadata = {
    'training_date': datetime.now().isoformat(),
    'dataset_size': len(df),
    'features': feature_cols,
    'models': {}
}

for target_name, description in targets.items():
    print(f"\n[{list(targets.keys()).index(target_name) + 2}/6] Training model for {description}...")
    
    y = df[target_name]
    
    # Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train Random Forest model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    print(f"   Training Random Forest (100 trees)...")
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"   Performance: R² = {r2:.4f}, MSE = {mse:.6f}")
    
    # Get feature importances
    feature_importance = dict(zip(feature_cols, model.feature_importances_))
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"   Top features: {', '.join([f[0] for f in top_features])}")
    
    # Save model
    model_path = f'models/{target_name}_model.pkl'
    joblib.dump(model, model_path)
    print(f"   ✓ Model saved to {model_path}")
    
    models[target_name] = model
    metadata['models'][target_name] = {
        'description': description,
        'r2_score': float(r2),
        'mse': float(mse),
        'top_features': [{'name': f[0], 'importance': float(f[1])} for f in top_features],
        'model_path': model_path
    }

# Save metadata
print(f"\n[6/6] Saving training metadata...")
with open('models/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"   ✓ Metadata saved to models/metadata.json")

print("\n" + "=" * 60)
print("Training Complete!")
print("=" * 60)
print(f"\nTrained {len(models)} models:")
for name, desc in targets.items():
    r2 = metadata['models'][name]['r2_score']
    print(f"  • {name}: {desc} (R² = {r2:.4f})")

print(f"\nModels are ready for inference in the BioSentience web application.")
print(f"All models saved in: models/")
print("=" * 60)
