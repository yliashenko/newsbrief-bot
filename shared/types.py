from typing import TypedDict

class TelegramPost(TypedDict):
    id: int
    text: str
    channel: str

class SummaryEntry(TypedDict):
    title: str
    summary: str