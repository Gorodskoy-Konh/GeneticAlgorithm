from datetime import time

class Assignee():
    def __init__(self, schedule: list[list[list[time]]], backend_id: int = None, stack: set[str]=set()) -> None:
        self.stack = stack
        self.schedule = schedule
        self.backend_id = backend_id

    def set_id(self, id: int):
        self.id = id 