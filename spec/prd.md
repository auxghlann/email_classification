# Product Requirements Document (PRD)

## Overview
The Email Classification service is a FastAPI-based REST API that classifies incoming email text into "spam" or "not spam" using a pre-trained Logistic Regression machine learning model.

## Goals & Objectives
- Primary Goal: Deploy a machine learning model through an API using FastAPI.
- Deliver high accuracy classification using a 3,000 word feature vocabulary.
- Expose a clean, non-redundant Pydantic response schema (`is_spam` boolean and `confidence` score).

## User Stories & Features
- [x] **POST /api/v1/classify**: Accepts raw email text (`text: str`) and returns classification results:
  - `is_spam`: boolean indicating spam status (`True` if spam, `False` otherwise).
  - `confidence`: float probability score for the prediction.
- [x] **GET /**: Health check status endpoint.

## Scope & Out-of-Scope
- **In-Scope**: Text feature extraction, model inference, FastAPI endpoints, automated pytest suite.
- **Out-of-Scope**: Online model re-training during API calls, database persistence.
