
from pydantic import BaseModel,Field
from typing import Optional, List, Literal

class Zone(BaseModel):
    name: str = Field(...)
    x: int = Field(...)
    y: int = Field(...)
    color: Optional[str] = None
    zone_type: Literal["normal", "blocked", "restricted", "priority"] = "normal"
    max_drones: int = Field(default=1, gt=0)


class Start_hub(Zone):
    pass


class Hub(Zone):
    pass


class End_hub(Zone):
    pass
