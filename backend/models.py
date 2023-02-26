from pydantic import BaseModel


class Message(BaseModel):
    id: int
    timestamp: float
    altitude: float
