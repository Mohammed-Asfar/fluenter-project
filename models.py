from pydantic import BaseModel, ConfigDict


class RewrittenTextModel(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Only allow defined fields
    rewritten_text: str
