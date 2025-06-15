from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class FormResponse(BaseModel):
    form_id: str
    responses: Dict[str, Any] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
