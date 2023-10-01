from datetime import datetime, timedelta
import random
from .Assignee import Assignee

ORDER_LIMIT = 100000

class Node():
    def __init__(self, deadline: datetime, duration: timedelta, id:int, assignee: Assignee=None, children=None, parents=None, order: int=None, stack: set[str]=set(), fixed_assignee:bool=False, project = None) -> None:
        self.children = children
        self.parents = parents
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.fixed_assignee = fixed_assignee
        self.id = id
        self.stack = stack
        self.start = None
        self.order = order if order is not None else int(random.random() * ORDER_LIMIT)
        self.project = project

    def copy(self):
        return Node(self.deadline, self.duration, self.id, self.assignee, self.children, self.parents, order=self.order)

    def __str__(self):
        # if self.child :
        #     return f"ID:{self.id}, Assignee:{self.assignee.id}, Duration:{self.duration}, Child:NO"
        return f"ID:{self.id}, Assignee:{self.assignee.id}, Duration:{self.duration}, Start:{self.start}"
    
    def stack_difference(self):
        return len(self.stack.difference(self.assignee.stack))
    
    def set_start_time(self, start):
        self.start = start