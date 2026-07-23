# System Architecture

## Overview
The application is a lightweight FastAPI web service that loads a pre-trained `scikit-learn` Logistic Regression model at startup and serves classification predictions via a RESTful endpoint.

## Technology Stack
- **Language**: Python 3.13+
- **Framework**: FastAPI
- **Machine Learning**: `scikit-learn`, `pandas`, `joblib`
- **Package Manager**: `uv`
- **Testing**: `pytest`, `httpx` (FastAPI TestClient)

## System Components & Data Flow

```
[ Client Request ]
       |
       v
 [ POST /api/v1/classify ] (FastAPI Router in app/api/v1/classifier_api.py)
       |
       v
 [ EmailRequest Pydantic Validation ] (app/api/v1/model.py)
       |
       v
 [ ClassifierService ] (app/services/classifier_service.py)
       |---> Text Tokenization & 3,000-Word Frequency Extraction
       |---> Scikit-Learn Model Inference (pkl_files/spam_model.pkl)
       v
 [ EmailClassificationResponse ] (JSON payload returned to client)
```

## Directory Structure
```
email_classification/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── classifier_api.py
│   │       ├── classifier_apy.py (wrapper)
│   │       └── model.py
│   └── services/
│       └── classifier_service.py
├── pkl_files/
│   ├── feature_names.pkl
│   └── spam_model.pkl
├── tests/
│   └── test_classifier_api.py
├── main.py
├── pyproject.toml
└── uv.lock
```
