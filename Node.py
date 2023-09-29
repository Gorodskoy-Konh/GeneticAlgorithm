from datetime import datetime, timedelta
from Assignee import Assigner

class Node():
    def __init__(self, deadline: datetime, duration: timedelta, id:int, assignee: Assigner=None, order:int=1, child=None, parent=None) -> None:
        self.parent = parent
        self.child = child
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.order = order
        self.id = id