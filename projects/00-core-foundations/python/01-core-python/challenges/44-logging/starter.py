"""Challenge 44 starter — fill in the bodies (never return working code)."""
from __future__ import annotations


def level_rank(level_name: str) -> int:
    raise NotImplementedError


def should_log(configured: str, event: str) -> bool:
    raise NotImplementedError


def make_logger(name: str, level: str):
    raise NotImplementedError


class CorrelatedLogger:
    def __init__(self, name: str, request_id: str) -> None:
        raise NotImplementedError

    def info(self, msg: str) -> None:
        raise NotImplementedError

    def error(self, msg: str) -> None:
        raise NotImplementedError

    def captured(self) -> str:
        raise NotImplementedError
