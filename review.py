from dataclasses import dataclass


@dataclass
class Review:
    userName: str
    userImage: str
    content: str
    score: int
    appVersion: str
    at: str