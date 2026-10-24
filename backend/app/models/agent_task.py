from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class AgentStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"


class TaskStatus(str, PyEnum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    role = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE, nullable=False)
    model_provider = Column(String(50), nullable=True)
    model_name = Column(String(100), nullable=True)
    budget_limit = Column(Integer, default=0, nullable=False)  # in cents
    budget_used = Column(Integer, default=0, nullable=False)
    parent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    parent = relationship("Agent", remote_side=[id], backref="children")
    assigned_tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assignee_id")
    created_tasks = relationship("Task", back_populates="creator", foreign_keys="Task.creator_id")

    __table_args__ = (Index("ix_agents_status", "status"),)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Integer, default=0, nullable=False)
    assignee_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    creator_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    budget_limit = Column(Integer, default=0, nullable=False)
    budget_used = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    assignee = relationship("Agent", back_populates="assigned_tasks", foreign_keys=[assignee_id])
    creator = relationship("Agent", back_populates="created_tasks", foreign_keys=[creator_id])
    parent_task = relationship("Task", remote_side=[id], backref="subtasks")

    __table_args__ = (
        Index("ix_tasks_status", "status"),
        Index("ix_tasks_assignee", "assignee_id"),
    )


class TaskComment(Base):
    __tablename__ = "task_comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    task = relationship("Task", backref="comments")
    agent = relationship("Agent")
