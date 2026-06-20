from pydantic import BaseModel, Field
from typing import Optional, Literal


class Zone(BaseModel):
    """Represents a zone in the drone navigation network.

    Attributes:
        name: Unique identifier for the zone.
        x: X coordinate of the zone.
        y: Y coordinate of the zone.
        color: Optional display color for visual representation.
        zone_type: Type of zone affecting movement cost.
        max_drones: Maximum drones allowed simultaneously.
    """

    name: str = Field(...)
    x: int = Field(...)
    y: int = Field(...)
    color: Optional[str] = None
    zone_type: Literal[
        "normal", "blocked", "restricted", "priority"
    ] = "normal"
    max_drones: int = Field(default=1, gt=0)


class Start_hub(Zone):
    """Represents the starting zone of the simulation."""

    pass


class Hub(Zone):
    """Represents a regular intermediate zone."""

    pass


class End_hub(Zone):
    """Represents the destination zone of the simulation."""

    pass


class Connection(BaseModel):
    """Represents a bidirectional connection between two zones.

    Attributes:
        zone1: Name of the first zone.
        zone2: Name of the second zone.
        max_link_capacity: Maximum drones traversing simultaneously.
    """

    zone1: str = Field(...)
    zone2: str = Field(...)
    max_link_capacity: int = Field(default=1, gt=0)


class Drone(BaseModel):
    """Represents a drone navigating through the zone network.

    Attributes:
        id: Unique positive identifier for the drone.
        current_position: Name of the zone the drone currently occupies.
        path: Ordered list of zone names the drone must follow.
    """

    id: int = Field(..., gt=0)
    current_position: str = Field(...)
    path: list[str] = Field(...)
