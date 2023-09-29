from datetime import datetime, timedelta

class Node():
    def __init__(self, depend_on, deadline: datetime, duration: timedelta, assigner=None) -> None:
        self.depend_on = depend_on
        self.deadline = deadline
        self.duration = duration
        self.assigner = assigner