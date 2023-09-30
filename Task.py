from datetime import datetime, timedelta
from Assignee import Assignee
from Node import Node

class Task():
    def __init__(self, deadline: datetime, duration: timedelta, depend_on, id: int, assignee: Assignee, backend_id: int) -> None:
        self.deadline = deadline
        self.duration = duration
        self.depend_on = depend_on
        self.assignee = assignee
        self.parent = None
        if not self.depend_on is None:
            self.depend_on.parent = self
        self.id = id
        self.backend_id