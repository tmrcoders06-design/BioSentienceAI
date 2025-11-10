# BioSentience

**Advanced Biological Data Analysis Platform with ML-Powered Predictions**

BioSentience is a web-based biological data analysis system that uses real machine learning models to predict health indices, mutation risks, and adaptation scores from biological measurements. The platform provides explainable AI insights and interactive simulations to explore how biological parameters affect outcomes.

---

## 🚀 Features

- **Real ML Models**: Random Forest models trained on biological data (not fake logic or hardcoded responses)
- **Multi-Target Prediction**: Simultaneously predicts:
  - Health Index (overall biological wellness)
  - Mutation Risk (genetic instability probability)
  - Adaptation Score (environmental resilience)
- **Explainable AI**: Feature importance analysis with natural language explanations
- **Interactive Simulations**: Vary biological parameters and visualize projected outcomes over time
- **CSV Upload**: Accepts biological data files for batch analysis
- **Futuristic UI**: Glassmorphism design with neon accents and Chart.js visualizations
- **Download Reports**: Export analysis results as JSON

---

## 📊 Dataset & Training

### Sample Dataset

The included sample dataset (`data/sample_biological_data.csv`) contains 50 synthesized biological measurements:

**Input Features (11 total):**
- **Gene Expression Levels**: BRCA1, TP53, EGFR, MYC, KRAS (normalized 0-1)
- **Cell Metrics**: Cell count, cell viability (0-1)
- **Environmental Variables**: pH level, temperature (°C), oxygen level (%), glucose level (mmol/L)

**Target Variables (3 total):**
- **Health Index**: 0-1 scale (higher = better overall health)
- **Mutation Risk**: 0-1 scale (higher = greater genetic instability risk)
- **Adaptation Score**: 0-1 scale (higher = better environmental adaptation)

**Dataset Source**: Synthesized data for demonstration purposes. Values are biologically plausible ranges but not from real clinical studies.

### Model Training

Models are trained using the `train.py` script:

```bash
python train.py
```

**Training Pipeline:**
1. Loads biological dataset from `data/sample_biological_data.csv`
2. Splits data (80% training, 20% testing)
3. Trains 3 separate Random Forest models (one per target variable)
4. Evaluates performance (R² score, MSE)
5. Saves models to `models/` directory with metadata

**Model Performance:**
- Health Index Model: R² > 0.98
- Mutation Risk Model: R² > 0.98
- Adaptation Score Model: R² > 0.98

**Model Specifications:**
- Algorithm: Random Forest Regressor (scikit-learn)
- Trees: 100 per model
- Max Depth: 10
- Min Samples Split: 5
- Features: 11 biological measurements

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Flask (web framework)
- pandas (data manipulation)
- numpy (numerical computing)
- scikit-learn (machine learning)
- joblib (model serialization)

**Frontend:**
- HTML5 / CSS3 / JavaScript (ES6+)
- Chart.js 4.4.0 (data visualization)
- Glassmorphism UI design
- Responsive layout

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager

### 1. Install Dependencies

```bash
pip install flask pandas numpy scikit-learn
```

Or use the package manager:

```bash
uv add flask pandas numpy scikit-learn
```

### 2. Train Models

Before running the application, train the ML models:

```bash
python train.py
```

This will create:
- `models/health_index_model.pkl`
- `models/mutation_risk_model.pkl`
- `models/adaptation_score_model.pkl`
- `models/metadata.json`

### 3. Run Application

```bash
python app.py
```

The application will start on `http://0.0.0.0:5000`

---

## 🎯 Usage

### 1. Upload Data

**Option A: Upload CSV File**
- Click the upload area or drag a CSV file
- Required columns: All 11 input features (gene expressions, cell metrics, environmental variables)
- Preview shows first 5 rows

**Option B: Use Sample Data**
- Click "Use Sample Data" button
- Loads pre-configured example from training dataset

### 2. Analyze

- Click "Analyze Data" button
- System validates input and runs predictions
- Results show:
  - Three prediction scores with confidence levels
  - Color-coded progress bars
  - Natural language explanation
  - Top contributing features

### 3. Simulate

- Select a biological parameter to vary
- Adjust variation range (±10% to ±50%)
- Click "Run Simulation"
- View interactive Chart.js visualization showing how predictions change

### 4. Download Report

- Click "Download Report (JSON)" to export analysis results
- Includes predictions, explanations, and input data

---

## 📁 Project Structure

```
biosentience/
├── app.py                  # Flask web application
├── train.py                # ML model training pipeline
├── data/
│   └── sample_biological_data.csv  # Training dataset
├── models/
│   ├── health_index_model.pkl
│   ├── mutation_risk_model.pkl
│   ├── adaptation_score_model.pkl
│   └── metadata.json
├── templates/
│   └── index.html          # Main web page
├── static/
│   ├── css/
│   │   └── style.css       # Glassmorphism UI styles
│   └── js/
│       └── app.js          # Frontend application logic
├── uploads/                # User-uploaded CSV files
└── README.md
```

---

## ⚠️ Important Disclaimers & Limitations

### Model Limitations

1. **Demonstration Purpose**: Models are trained on synthesized data for educational/research purposes
2. **Not Medical Advice**: Predictions are ML model outputs, NOT clinical diagnoses or medical recommendations
3. **Limited Training Data**: Only 50 samples in training set (real-world models need thousands)
4. **Simplified Biology**: Real biological systems are far more complex than 11 input features
5. **No Clinical Validation**: Models have not been validated against real clinical outcomes

### Data Constraints

- **Input Ranges**: Features should be within biologically plausible ranges (0-1 for genes, realistic values for cell metrics)
- **Missing Values**: Not supported - all 11 features required
- **File Format**: CSV only, with exact column names matching training data

### Production Deployment

- **Development Server**: Flask's built-in server is NOT production-ready
- **Security**: No authentication, rate limiting, or input sanitization for production
- **Scalability**: Models loaded in memory - not optimized for concurrent users
- **Cache Control**: Configured for development (no-cache headers recommended for production)

**For Production Use:**
- Deploy with Gunicorn/uWSGI
- Add authentication (OAuth, JWT)
- Implement rate limiting
- Add input validation and sanitization
- Use proper secrets management
- Add monitoring and logging
- Consider model versioning system

---

## 🔬 Reproducibility

### Training Reproducibility

The training pipeline is fully reproducible:

1. **Fixed Random Seed**: `random_state=42` in all models and splits
2. **Deterministic Splits**: Same 80/20 train/test split every time
3. **Saved Metadata**: `models/metadata.json` includes training date, features, performance
4. **Version Control**: All code and data in repository

To reproduce training:

```bash
# Delete existing models
rm models/*.pkl models/*.json

# Re-train
python train.py

# Models will have identical R² scores and feature importances
```

### Dataset Modifications

To use your own biological data:

1. Create CSV with same 11 feature columns
2. Add target columns if training new models
3. Update `data/sample_biological_data.csv`
4. Run `python train.py`
5. Restart Flask app

---

## 🧪 API Endpoints

### `POST /api/upload`
Upload CSV file for analysis
- **Input**: FormData with CSV file
- **Output**: Preview with rows, columns, data sample

### `POST /api/analyze`
Run ML predictions on data
- **Input**: `{ "data": { ...features... } }`
- **Output**: Predictions, confidence scores, explanations

### `POST /api/simulate`
Simulate parameter variation
- **Input**: `{ "base_features": {...}, "vary_feature": "gene_BRCA1", "steps": 15, "variation_range": 0.3 }`
- **Output**: Trajectory data for visualization

### `GET /api/sample-data`
Get sample data for testing
- **Output**: `{ "data": {...}, "note": "Demo data" }`

---

## 📝 License & Attribution

**Dataset**: Synthesized biological data (no real patient data)

**Code**: Built with open-source libraries (Flask, scikit-learn, Chart.js)

**Educational Use**: This project is for educational and research purposes. Not approved for clinical/medical use.

---

## 🤝 Contributing

Improvements welcome:
- Add real biological datasets (with proper attribution)
- Implement SHAP for advanced explainability
- Add more visualization types (3D with Three.js)
- Implement user authentication
- Add PDF report generation
- Support additional file formats (FASTA, VCF)

---

## 📧 Contact

For questions about the ML models, training pipeline, or biological data requirements, refer to the code documentation in `train.py` and `app.py`.

---

**Built with ❤️ for transparent, reproducible biological data analysis**
