from pydantic import BaseModel
from .parser.currency import Code


class Rate(BaseModel):
    pair: str
    rate: float


class HealthStatus(BaseModel):
    status: str
