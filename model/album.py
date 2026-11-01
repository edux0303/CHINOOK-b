from dataclasses import dataclass, field


@dataclass
class Album:
    id: int
    title: str
    artistId: int
    numBrani: int = 0
    brani: set = field(default_factory=set)
    generi: set = field(default_factory=set)
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.title

