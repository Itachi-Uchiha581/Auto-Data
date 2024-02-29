from dataclasses import dataclass, asdict


@dataclass
class TopicHistory:
    Chats: list
    topic: str
    threads: int
    length: int

    def to_dict(self):
        return asdict(self)
