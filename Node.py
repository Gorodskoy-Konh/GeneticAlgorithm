from datetime import datetime, timedelta
import random
from Assignee import Assignee

ORDER_LIMIT = 100000

class Node():
    def __init__(self, deadline: datetime, duration: timedelta, id:int, assignee: Assignee=None, child=None, parent=None) -> None:
        self.child = child
        self.parent = parent
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.id = id
        self.order = int(random.random() * ORDER_LIMIT)

    def copy(self):
        return Node(self.deadline, self.duration, self.id, self.assignee, self.child, self.parent)
