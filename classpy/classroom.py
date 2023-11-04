from dataclasses import dataclass


@dataclass
class ClassRoom:
    name: str
    url: str

    def __post_init__(self) -> None:
        checks = (
            isinstance(self.name, str),
            isinstance(self.url, str),
        )
        if not all(checks):
            raise TypeError
