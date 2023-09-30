from datetime import datetime, timedelta
import random
import copy
from Assignee import Assignee

ORDER_LIMIT = 100000

class Node():
    def __init__(self, deadline: datetime, duration: timedelta, id:int, assignee=None, child=None, parent=None, order=None) -> None:
        self.child = child
        self.parent = parent
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.id = id
        self.order = order if order is not None else int(random.random() * ORDER_LIMIT)

    def copy(self):
        return copy.copy(self)