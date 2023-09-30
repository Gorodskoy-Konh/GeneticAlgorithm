from datetime import datetime, timedelta
from .Assignee import Assignee
from .Node import Node

class Task():
    def __init__(self, deadline: datetime, duration: timedelta, assignee: Assignee, backend_id: int = None, stack: set[str]={}, start: timedelta=None) -> None:
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.depend_on = []
        self.parents = []
        self.backend_id = backend_id
        self.stack = stack
        self.start = start
    
    def set_depend_on(self, depend_on):
        self.depend_on = depend_on
        for parent in self.depend_on:
            parent.parents.append(self)
    
    def set_id(self, id: int):
        self.id = id