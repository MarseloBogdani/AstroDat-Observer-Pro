from dataclasses import dataclass

@dataclass
class ObservationDTO:
    id: int | None = None
    object: str = ""
    date: str = ""
    equipment: str = ""
    note: str = ""