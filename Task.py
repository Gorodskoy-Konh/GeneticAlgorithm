from datetime import datetime, timedelta
from Assignee import Assignee
from Node import Node

class Task():
    def __init__(self, deadline: datetime, duration: timedelta, assignee: Assignee, backend_id: int = None, stack: set[str]={}) -> None:
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.depend_on = None
        self.parent = None
        self.backend_id = backend_id
        self.stack = stack
    
    def set_depend_on(self, depend_on):
        self.depend_on = depend_on
        if not self.depend_on is None:
            self.depend_on.parent = self
    
    def set_id(self, id: int):
        self.id = id