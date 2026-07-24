from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    text: str = Field(..., description="Raw text of the email to classify")


class EmailClassificationResponse(BaseModel):
    is_spam: bool = Field(..., description="True if email is spam, False otherwise")
    confidence: float = Field(..., description="Probability score of the prediction")
