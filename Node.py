from datetime import datetime, timedelta
import random
import copy

ORDER_LIMIT = 100000

class Node():
    def __init__(self, deadline: datetime, duration: timedelta, id:int, assignee=None, child=None, parent=None) -> None:
        self.child = child
        self.parent = parent
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.id = id
        self.order = int(random.random() * ORDER_LIMIT)

    def copy(self):
        copy.copy(self)