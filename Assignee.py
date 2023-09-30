from datetime import time

class Assignee():
    def __init__(self, id: int, stack: set[str], schedule: list[list[list[time]]], backend_id: int) -> None:
        self.id = id
        self.stack = stack
        self.schedule = schedule
        self.backend_id = backend_id