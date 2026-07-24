# Architectural Decision Records (ADRs)

## ADR-001: Initial Architecture and Tooling Setup
- **Status**: Accepted
- **Context**: Setting up email classification service.
- **Decision**: Use FastAPI and `uv` package manager.
- **Consequences**: Standardized dependencies and lightweight fast execution.

## ADR-002: Streamlit Dashboard Frontend
- **Status**: Accepted
- **Context**: Providing a user-friendly interactive web interface for non-developer testing and visual analytics.
- **Decision**: Use Streamlit (`streamlit_app.py`) as a client consuming the FastAPI REST backend over HTTP, with automatic fallback to local `ClassifierService` if the API is offline.
- **Consequences**: Decoupled architecture preserving API functionality while delivering interactive UI metrics and feature breakdown tables.

## ADR-003: Schema Package Decoupling
- **Status**: Accepted
- **Context**: Prevent circular imports between `app.api.v1` and `app.services.classifier_service`.
- **Decision**: Move Pydantic models (`EmailRequest`, `EmailClassificationResponse`) to `app/schemas/email_schema.py`.
- **Consequences**: Clean dependency hierarchy where schemas have zero internal package dependencies, eliminating circular import exceptions.
