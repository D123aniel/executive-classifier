from pydantic import BaseModel, ConfigDict, Field, field_validator


class PredictionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=12_000)
    response: str = Field(min_length=1, max_length=12_000)

    @field_validator("question", "response")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Text must contain at least one non-whitespace character.")
        return stripped_value


class PredictionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    label: str
    scores: dict[str, float]
    margin: float
    review_recommended: bool = Field(serialization_alias="reviewRecommended")
    truncated: bool
    token_count: int = Field(serialization_alias="tokenCount")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool = Field(serialization_alias="modelLoaded")
