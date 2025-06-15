from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class FieldSchema(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    label: str
    type: Literal["text", "number", "dropdown"]
    options: Optional[List[str]] = None            # dropdown only

class FormIn(BaseModel):
    title: str
    fields: List[FieldSchema]

class Form(FormIn):
    form_id: str = Field(default_factory=lambda: uuid4().hex)
    created_by: str = "admin"                      # minimal role demo
