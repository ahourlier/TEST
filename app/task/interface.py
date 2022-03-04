from typing import Optional
from datetime import date
from mypy_extensions import TypedDict


class TaskInterface(TypedDict):
    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    author_id: Optional[int]
    author: Optional[dict]
    assignee_id: Optional[int]
    assignee: Optional[dict]
    status: Optional[str]
    step_id: Optional[str]
    reminder_date: Optional[date]
    date: Optional[date]
    task_type: str
