from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .model_service import ModelService
from .schemas import HealthResponse, PredictionRequest, PredictionResponse


@lru_cache
def get_model_service() -> ModelService:
    settings = get_settings()
    return ModelService(
        model_path=settings.model_path,
        top_score_review_threshold=settings.top_score_review_threshold,
        margin_review_threshold=settings.margin_review_threshold,
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    application = FastAPI(
        title=resolved_settings.app_name,
        version="0.1.0",
        description=(
            "Classifies an executive response as Direct, Partially Evasive, "
            "or Fully Evasive relative to an analyst question."
        ),
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.origin_list,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    @application.get("/health", response_model=HealthResponse)
    def health(
        service: ModelService = Depends(get_model_service),
    ) -> HealthResponse:
        return HealthResponse(status="ok", model_loaded=service.is_loaded)

    @application.post(
        "/predict",
        response_model=PredictionResponse,
        response_model_by_alias=True,
    )
    def predict(
        request: PredictionRequest,
        service: ModelService = Depends(get_model_service),
    ) -> PredictionResponse:
        try:
            prediction = service.predict(request.question, request.response)
        except FileNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="The model artifact is not available.",
            ) from error

        return PredictionResponse(
            label=prediction.label,
            scores=prediction.scores,
            margin=prediction.margin,
            review_recommended=prediction.review_recommended,
            truncated=prediction.truncated,
            token_count=prediction.token_count,
        )

    return application


app = create_app()
