# BioSentience Project

## Overview
BioSentience is a Flask-based biological data analysis platform that uses real machine learning models to analyze biological data and produce explainable predictions with interactive simulations.

**Project Type**: Web Application (Flask + ML)  
**Status**: Fully Functional MVP  
**Created**: November 10, 2025

## Purpose & Goals
- Analyze biological data (gene expressions, cell metrics, environmental variables) using real ML models
- Provide explainable AI predictions for health index, mutation risk, and adaptation scores
- Enable interactive simulations to explore how biological parameters affect outcomes
- Maintain transparency: all predictions from real models, not fake logic

## Current State
✅ **Complete & Operational**
- 3 trained Random Forest models (>98% R² accuracy)
- Flask web server with 5 API endpoints
- Futuristic glassmorphism UI with Chart.js visualizations
- Interactive simulation mode with parameter variation
- JSON report download functionality
- Comprehensive documentation

## Recent Changes

### November 10, 2025 - Initial Build
- Created project structure (app.py, train.py, templates/, static/, data/, models/)
- Generated sample biological dataset (50 samples, 14 features)
- Built reproducible ML training pipeline (train.py)
- Trained 3 Random Forest models for health_index, mutation_risk, adaptation_score
- Created Flask application with API endpoints: /upload, /analyze, /simulate, /explain, /sample-data
- Built glassmorphism frontend with HTML/CSS/JS
- Implemented Chart.js visualizations for predictions and simulations
- Added feature importance explainability with natural language summaries
- Created interactive simulation sliders with animated trajectory charts
- Added JSON report download
- Wrote comprehensive README with dataset sources, training reproducibility, and model limitations
- Configured Flask workflow on port 5000

## Project Architecture

### Backend (Python/Flask)
- **app.py**: Main Flask application with API endpoints
- **train.py**: ML model training pipeline (reproducible)
- **models/**: Saved Random Forest models (.pkl) and metadata (.json)
- **data/**: Sample biological dataset (CSV)

### Frontend
- **templates/index.html**: Main web interface
- **static/css/style.css**: Glassmorphism UI with neon accents
- **static/js/app.js**: Frontend logic with Chart.js integration

### ML Pipeline
- Algorithm: Random Forest Regressor (scikit-learn)
- Input Features: 11 biological measurements
  - Gene expression: BRCA1, TP53, EGFR, MYC, KRAS
  - Cell metrics: cell_count, cell_viability
  - Environmental: ph_level, temperature, oxygen_level, glucose_level
- Output Targets: health_index, mutation_risk, adaptation_score
- Training: 80/20 split, random_state=42 for reproducibility

### Key Dependencies
- Flask (web framework)
- pandas (data manipulation)
- numpy (numerical computing)
- scikit-learn (machine learning)
- Chart.js (frontend visualization via CDN)

## Features Implemented

### Core Functionality
1. **CSV Upload**: Accept biological data files with validation
2. **Sample Data**: Demo data from training set
3. **ML Predictions**: Real-time inference with 3 models
4. **Explainability**: Feature importance + natural language summaries
5. **Interactive Simulation**: Vary parameters, visualize trajectories
6. **Download Reports**: Export analysis as JSON

### UI/UX
- Futuristic glassmorphism design
- Neon accent colors (cyan, magenta, purple)
- Animated background stars
- Color-coded risk indicators
- Responsive layout
- Chart.js line charts for simulations

## API Endpoints
- `POST /api/upload`: CSV file upload with preview
- `POST /api/analyze`: Run ML predictions on data
- `POST /api/simulate`: Parameter variation simulation
- `POST /api/explain`: Get detailed feature importance
- `GET /api/sample-data`: Retrieve demo data

## Dataset & Training

### Sample Dataset
- **Source**: Synthesized biological data (demonstration purposes)
- **Size**: 50 samples
- **Features**: 11 input features, 3 target variables
- **Format**: CSV with biologically plausible value ranges

### Model Performance
- Health Index Model: R² = 0.9844
- Mutation Risk Model: R² = 0.9839
- Adaptation Score Model: R² = 0.9828

### Reproducibility
- Fixed random seed (42) for deterministic results
- Training script saves metadata.json with full pipeline info
- All models can be retrained: `python train.py`

## Important Notes

### Disclaimers
⚠️ **Not Medical Advice**: Models are for research/educational purposes only  
⚠️ **Demo Data**: Training data is synthesized, not from real clinical studies  
⚠️ **Development Server**: Flask debug server - use Gunicorn for production

### Model Limitations
- Only 50 training samples (real models need thousands)
- Simplified biology (11 features vs. complex reality)
- No clinical validation
- Requires exact feature names and ranges

## File Structure
```
/
├── app.py                  # Flask web application
├── train.py                # ML training pipeline
├── README.md               # Comprehensive documentation
├── .gitignore             # Python/Flask ignore patterns
├── data/
│   └── sample_biological_data.csv
├── models/
│   ├── health_index_model.pkl
│   ├── mutation_risk_model.pkl
│   ├── adaptation_score_model.pkl
│   └── metadata.json
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/app.js
└── uploads/               # User CSV uploads
    └── .gitkeep
```

## Running the Application

### Train Models
```bash
python train.py
```

### Start Web Server
```bash
python app.py
```

Application runs on: `http://0.0.0.0:5000`

## Future Enhancements
- Integrate SHAP for advanced explainability
- Add PDF report generation
- Implement 3D visualization with Three.js
- Support additional file formats (FASTA, VCF)
- User authentication for saved analyses
- Production deployment configuration
- Expanded training dataset
- Model versioning system

## License & Attribution
- Code: Open source libraries (Flask, scikit-learn, Chart.js)
- Data: Synthesized (no real patient data)
- Purpose: Educational and research use only

---

**Last Updated**: November 10, 2025  
**Version**: 1.0.0  
**Status**: MVP Complete & Operational
