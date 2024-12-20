from pydantic import BaseModel
from typing import Literal


class ResultsDTO(BaseModel):
    status: bool
    text: str


