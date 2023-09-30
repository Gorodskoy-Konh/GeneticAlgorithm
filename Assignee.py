from datetime import time

class Assignee():
    def __init__(self, stack: set[str], schedule: list[list[list[time]]], backend_id: int = None) -> None:
        self.stack = stack
        self.schedule = schedule
        self.backend_id = backend_id

    def set_id(self, id: int):
        self.id = id 