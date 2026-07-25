import asyncio

from httpx import ASGITransport, AsyncClient, Response

from app.main import create_app, get_model_service
from app.model_service import Prediction


class FakeModelService:
    is_loaded = True

    def predict(self, question: str, response: str) -> Prediction:
        assert question == "What drove the margin decline?"
        assert response == "Higher freight costs reduced margin by 2%."
        return Prediction(
            label="Direct",
            scores={
                "Direct": 0.91,
                "Partially Evasive": 0.07,
                "Fully Evasive": 0.02,
            },
            margin=0.84,
            review_recommended=False,
            truncated=False,
            token_count=24,
        )


def make_app():
    application = create_app()
    application.dependency_overrides[get_model_service] = FakeModelService
    return application


def request(method: str, path: str, **kwargs) -> Response:
    async def send_request() -> Response:
        transport = ASGITransport(app=make_app())
        async with AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            return await client.request(method, path, **kwargs)

    return asyncio.run(send_request())


def test_health_reports_model_state() -> None:
    response = request("GET", "/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "modelLoaded": True}


def test_predict_returns_classifier_result() -> None:
    response = request(
        "POST",
        "/predict",
        json={
            "question": "What drove the margin decline?",
            "response": "Higher freight costs reduced margin by 2%.",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "label": "Direct",
        "scores": {
            "Direct": 0.91,
            "Partially Evasive": 0.07,
            "Fully Evasive": 0.02,
        },
        "margin": 0.84,
        "reviewRecommended": False,
        "truncated": False,
        "tokenCount": 24,
    }


def test_predict_rejects_empty_text() -> None:
    response = request(
        "POST",
        "/predict",
        json={"question": "", "response": ""},
    )

    assert response.status_code == 422


def test_predict_rejects_whitespace_only_text() -> None:
    response = request(
        "POST",
        "/predict",
        json={"question": "   ", "response": "\n\t"},
    )

    assert response.status_code == 422
