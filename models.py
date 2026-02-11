from dataclasses import dataclass

@dataclass
class ObservationDTO:
    """
    Independent Data Transfer Object.
    Uses 'object' to match your original naming convention.
    """
    id: int | None = None
    object: str = ""
    date: str = ""
    equipment: str = ""
    note: str = ""