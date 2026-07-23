from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Email Classification API"}


def test_classify_spam_email() -> None:
    spam_payload = {
        "text": "Subject: Congratulations! You won a free prize. Click here now for money cash dollar claim."
    }
    response = client.post("/api/v1/classify", json=spam_payload)
    assert response.status_code == 200

    data = response.json()
    assert "is_spam" in data
    assert "confidence" in data
    assert data["is_spam"] is True
    assert isinstance(data["confidence"], float)


def test_classify_ham_email() -> None:
    ham_payload = {
        "text": "Hi team, please find attached the report for our weekly meeting. Let me know if you have any questions."
    }
    response = client.post("/api/v1/classify", json=ham_payload)
    assert response.status_code == 200

    data = response.json()
    assert "is_spam" in data
    assert "confidence" in data
    assert data["is_spam"] is False
    assert isinstance(data["confidence"], float)


def test_classify_empty_email_payload() -> None:
    empty_payload = {"text": "   "}
    response = client.post("/api/v1/classify", json=empty_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email text payload cannot be empty or whitespace only."

