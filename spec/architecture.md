# System Architecture

## Overview
The application is a modular email classification system featuring a lightweight FastAPI web service and a Streamlit interactive dashboard. It loads a pre-trained `scikit-learn` Logistic Regression model at startup and serves predictions via RESTful endpoints or directly through the web UI.

## Technology Stack
- **Language**: Python 3.13+
- **Frameworks**: FastAPI, Streamlit
- **Machine Learning**: `scikit-learn`, `pandas`, `joblib`
- **Package Manager**: `uv`
- **Testing**: `pytest`, `httpx` (FastAPI TestClient)

## System Components & Data Flow

```
+------------------+         +----------------------------+
|   Streamlit UI   | ------->|   FastAPI REST Endpoint    |
| (streamlit_app)  |  HTTP   |  [POST /api/v1/classify]   |
+------------------+         +----------------------------+
         |                                  |
         | (Fallback)                       v
         |                      [ EmailRequest Validation ]
         |                     (app/schemas/email_schema.py)
         |                                  |
         +-----------------+----------------+
                           |
                           v
                 [ ClassifierService ]
          (app/services/classifier_service.py)
                           |
                           |---> Text Tokenization & 3,000-Word Frequency Extraction
                           |---> Scikit-Learn Model Inference (pkl_files/spam_model.pkl)
                           v
             [ EmailClassificationResponse ]
```

## Directory Structure
```
email_classification/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── classifier_api.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── email_schema.py
│   └── services/
│       └── classifier_service.py
├── docs/
│   └── recall/
│       └── recall_fastapi_router_service.html
├── pkl_files/
│   ├── feature_names.pkl
│   └── spam_model.pkl
├── spec/
│   ├── architecture.md
│   ├── decisions.md
│   └── prd.md
├── tests/
│   └── test_classifier_api.py
├── main.py
├── streamlit_app.py
├── pyproject.toml
└── uv.lock
```
