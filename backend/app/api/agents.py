from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.agent_task import Agent, Task, TaskComment, AgentStatus, TaskStatus
from app.api.schemas import (
    AgentCreate, AgentUpdate, AgentResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    TaskCommentCreate, TaskCommentResponse,
    HeartbeatRequest, HeartbeatResponse,
)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(agent_in: AgentCreate, db: Session = Depends(get_db)):
    agent = Agent(**agent_in.model_dump())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.get("", response_model=List[AgentResponse])
def list_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[AgentStatus] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Agent)
    if status:
        query = query.filter(Agent.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: int, agent_in: AgentUpdate, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    update_data = agent_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return None
