from pydantic import BaseModel, Field
from typing import List
from typing import Optional

class GoalRequest(BaseModel):
    goal: str

class TaskItem(BaseModel):
    step: str = Field(description="The category/phase of the task")
    task: str = Field(description="Brief title of the task")
    description: str = Field(description="Detailed description of what needs to be done")
    technologies: List[str] = Field(description="Recommended technologies/tools for this task")
    deliverables: List[str] = Field(description="Expected outputs/deliverables from this task")
    estimated_time: str = Field(description="Estimated time to complete this task")
    jira_issue: Optional[str] = None
    jira_link: Optional[str] = None
    github_issue: Optional[str] = None
    github_link: Optional[str] = None

class TaskList(BaseModel):
    tasks: List[TaskItem] = Field(description="List of detailed actionable subtasks")
