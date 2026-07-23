from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.model import EmailRequest, EmailClassificationResponse
from app.services.classifier_service import ClassifierService, get_classifier_service

router = APIRouter()


@router.post("/classify", response_model=EmailClassificationResponse)
def classify_email(
    payload: EmailRequest,
    service: ClassifierService = Depends(get_classifier_service),
) -> EmailClassificationResponse:
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email text payload cannot be empty or whitespace only.",
        )
    try:
        return service.classify(payload.text)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification service unavailable: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during email classification: {str(e)}",
        )

