from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from app.models.agent_task import AgentStatus, TaskStatus


class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    budget_limit: int = Field(default=0, ge=0)
    parent_id: Optional[int] = None
    status: Optional[AgentStatus] = None

    model_config = ConfigDict(protected_namespaces=())


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    budget_limit: Optional[int] = Field(None, ge=0)
    parent_id: Optional[int] = None

    model_config = ConfigDict(protected_namespaces=())


class AgentResponse(AgentBase):
    id: int
    status: AgentStatus
    budget_used: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: int = Field(default=0, ge=0)
    budget_limit: int = Field(default=0, ge=0)
    parent_task_id: Optional[int] = None

    model_config = ConfigDict(protected_namespaces=())


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(None, ge=0)
    assignee_id: Optional[int] = None
    budget_limit: Optional[int] = Field(None, ge=0)
    parent_task_id: Optional[int] = None

    model_config = ConfigDict(protected_namespaces=())


class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    assignee_id: Optional[int]
    creator_id: Optional[int]
    budget_used: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class TaskCommentBase(BaseModel):
    content: str = Field(..., min_length=1)

    model_config = ConfigDict(protected_namespaces=())


class TaskCommentCreate(TaskCommentBase):
    pass


class TaskCommentResponse(TaskCommentBase):
    id: int
    task_id: int
    agent_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class HeartbeatRequest(BaseModel):
    agent_id: int

    model_config = ConfigDict(protected_namespaces=())


class HeartbeatResponse(BaseModel):
    task: Optional[TaskResponse] = None
    message: str = "no_work"

    model_config = ConfigDict(protected_namespaces=())
