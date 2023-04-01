from pydantic import BaseModel


class Message(BaseModel):
    id: int
    timestamp: float
    altitude: float
    velocity: float
    acceleration: float
    latitude: float
    longitude: float
    temperature: float
    pressure: float