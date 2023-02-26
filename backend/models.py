from pydantic import BaseModel


class Message(BaseModel):
    id: int
    timestamp: str
    altitude: float
