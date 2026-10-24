@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None


@router.post("/{task_id}/assign/{agent_id}", response_model=TaskResponse)
def assign_task(task_id: int, agent_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.status != AgentStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Agent is not active")
    task.assignee_id = agent_id
    task.status = TaskStatus.ASSIGNED
    db.commit()
    db.refresh(task)
    return task


@router.post("/heartbeat", response_model=HeartbeatResponse)
def heartbeat(request: HeartbeatRequest, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == request.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.status != AgentStatus.ACTIVE:
        return HeartbeatResponse(message="agent_not_active")
    task = (
        db.query(Task)
        .filter(Task.assignee_id == agent.id, Task.status == TaskStatus.ASSIGNED)
        .order_by(Task.priority.desc(), Task.created_at)
        .first()
    )
    if not task:
        return HeartbeatResponse(message="no_work")
    task.status = TaskStatus.IN_PROGRESS
    db.commit()
    db.refresh(task)
    return HeartbeatResponse(task=task, message="work_assigned")


@router.post("/{task_id}/comments", response_model=TaskCommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(task_id: int, comment_in: TaskCommentCreate, agent_id: int = Query(...), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    comment = TaskComment(task_id=task_id, agent_id=agent_id, content=comment_in.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/{task_id}/comments", response_model=List[TaskCommentResponse])
def list_comments(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db.query(TaskComment).filter(TaskComment.task_id == task_id).order_by(TaskComment.created_at).all()
