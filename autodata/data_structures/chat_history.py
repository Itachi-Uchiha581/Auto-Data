from dataclasses import dataclass, asdict


@dataclass
class ChatHistory:
    messages: list[dict]
    model: str
    sub_topic: str
    system_prompt: str

    def to_dict(self):
        return asdict(self)
