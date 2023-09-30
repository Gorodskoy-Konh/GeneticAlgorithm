from datetime import datetime, timedelta
import random
from .Assignee import Assignee

ORDER_LIMIT = 100000

class Node():
    def __init__(self, deadline: datetime, duration: timedelta, id:int, assignee: Assignee=None, children=None, parents=None, order: int=None, stack: set[str]=set(), fixed_assignee:bool=False) -> None:
        self.children = children
        self.parents = parents
        self.deadline = deadline
        self.duration = duration
        self.assignee = assignee
        self.fixed_assignee = fixed_assignee
        self.id = id
        self.stack = stack
        self.order = order if order is not None else int(random.random() * ORDER_LIMIT)

    def copy(self):
        return Node(self.deadline, self.duration, self.id, self.assignee, self.children, self.parents)

    def __str__(self):
        # if self.child :
        #     return f"ID:{self.id}, Assignee:{self.assignee.id}, Duration:{self.duration}, Child:NO"
        return f"ID:{self.id}, Assignee:{self.assignee.id}, Duration:{self.duration}, Child:{self.children}"
    
    def stack_difference(self):
        return len(self.stack.difference(self.assignee.stack))