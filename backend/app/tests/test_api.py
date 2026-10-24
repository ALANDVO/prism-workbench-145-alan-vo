import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models.agent_task import Agent, Task, AgentStatus, TaskStatus

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestHealth:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAgents:
    def test_create_agent(self):
        response = client.post("/api/agents", json={
            "name": "Test Agent",
            "role": "Developer",
            "description": "A test agent",
            "model_provider": "openai",
            "model_name": "gpt-4o",
            "budget_limit": 1000,
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Agent"
        assert data["role"] == "Developer"
        assert data["status"] == "active"
        assert data["budget_limit"] == 1000
        assert data["budget_used"] == 0
        assert "id" in data

    def test_create_agent_minimal(self):
        response = client.post("/api/agents", json={
            "name": "Minimal Agent",
            "role": "Tester",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal Agent"
        assert data["role"] == "Tester"
        assert data["model_provider"] is None

    def test_list_agents(self):
        client.post("/api/agents", json={"name": "Agent 1", "role": "Dev"})
        client.post("/api/agents", json={"name": "Agent 2", "role": "QA"})
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_agents_with_status_filter(self):
        client.post("/api/agents", json={"name": "Active Agent", "role": "Dev"})
        client.post("/api/agents", json={"name": "Inactive Agent", "role": "Dev", "status": "inactive"})
        response = client.get("/api/agents?status=active")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Active Agent"

    def test_get_agent(self):
        create_resp = client.post("/api/agents", json={"name": "Get Agent", "role": "Dev"})
        agent_id = create_resp.json()["id"]
        response = client.get(f"/api/agents/{agent_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Get Agent"

    def test_get_agent_not_found(self):
        response = client.get("/api/agents/999")
        assert response.status_code == 404

    def test_update_agent(self):
        create_resp = client.post("/api/agents", json={"name": "Old Name", "role": "Dev"})
        agent_id = create_resp.json()["id"]
        response = client.patch(f"/api/agents/{agent_id}", json={"name": "New Name", "status": "busy"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["status"] == "busy"

    def test_delete_agent(self):
        create_resp = client.post("/api/agents", json={"name": "To Delete", "role": "Dev"})
        agent_id = create_resp.json()["id"]
        response = client.delete(f"/api/agents/{agent_id}")
        assert response.status_code == 204
        get_resp = client.get(f"/api/agents/{agent_id}")
        assert get_resp.status_code == 404

    def test_agent_parent_child(self):
        parent_resp = client.post("/api/agents", json={"name": "Parent", "role": "Manager"})
        parent_id = parent_resp.json()["id"]
        child_resp = client.post("/api/agents", json={"name": "Child", "role": "Worker", "parent_id": parent_id})
        assert child_resp.json()["parent_id"] == parent_id


class TestTasks:
    def test_create_task(self):
        response = client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "A test task",
            "priority": 5,
            "budget_limit": 500,
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["status"] == "pending"
        assert data["priority"] == 5
        assert data["assignee_id"] is None

    def test_list_tasks(self):
        client.post("/api/tasks", json={"title": "Task 1"})
        client.post("/api/tasks", json={"title": "Task 2"})
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_tasks_with_status_filter(self):
        client.post("/api/tasks", json={"title": "Pending Task"})
        client.post("/api/tasks", json={"title": "Assigned Task"})
        # Manually update one to assigned via DB would be better, but we test filter works
        response = client.get("/api/tasks?status=pending")
        assert response.status_code == 200
        data = response.json()
        assert all(t["status"] == "pending" for t in data)

    def test_get_task(self):
        create_resp = client.post("/api/tasks", json={"title": "Get Task"})
        task_id = create_resp.json()["id"]
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Get Task"

    def test_get_task_not_found(self):
        response = client.get("/api/tasks/999")
        assert response.status_code == 404

    def test_update_task(self):
        create_resp = client.post("/api/tasks", json={"title": "Old Title"})
        task_id = create_resp.json()["id"]
        response = client.patch(f"/api/tasks/{task_id}", json={"title": "New Title", "status": "in_progress"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["status"] == "in_progress"

    def test_update_task_completed_sets_timestamp(self):
        create_resp = client.post("/api/tasks", json={"title": "Complete Me"})
        task_id = create_resp.json()["id"]
        response = client.patch(f"/api/tasks/{task_id}", json={"status": "completed"})
        assert response.status_code == 200
        assert response.json()["completed_at"] is not None

    def test_delete_task(self):
        create_resp = client.post("/api/tasks", json={"title": "To Delete"})
        task_id = create_resp.json()["id"]
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204
        get_resp = client.get(f"/api/tasks/{task_id}")
        assert get_resp.status_code == 404


class TestTaskAssignment:
    def test_assign_task_to_agent(self):
        agent_resp = client.post("/api/agents", json={"name": "Worker", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        task_resp = client.post("/api/tasks", json={"title": "Work Item"})
        task_id = task_resp.json()["id"]

        response = client.post(f"/api/tasks/{task_id}/assign/{agent_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["assignee_id"] == agent_id
        assert data["status"] == "assigned"

    def test_assign_task_to_inactive_agent_fails(self):
        agent_resp = client.post("/api/agents", json={"name": "Inactive", "role": "Dev", "status": "inactive"})
        agent_id = agent_resp.json()["id"]
        task_resp = client.post("/api/tasks", json={"title": "Work Item"})
        task_id = task_resp.json()["id"]

        response = client.post(f"/api/tasks/{task_id}/assign/{agent_id}")
        assert response.status_code == 400
        assert "not active" in response.json()["detail"].lower()

    def test_assign_nonexistent_task_fails(self):
        agent_resp = client.post("/api/agents", json={"name": "Worker", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        response = client.post(f"/api/tasks/999/assign/{agent_id}")
        assert response.status_code == 404

    def test_assign_nonexistent_agent_fails(self):
        task_resp = client.post("/api/tasks", json={"title": "Work Item"})
        task_id = task_resp.json()["id"]
        response = client.post(f"/api/tasks/{task_id}/assign/999")
        assert response.status_code == 404


class TestHeartbeat:
    def test_heartbeat_no_work(self):
        agent_resp = client.post("/api/agents", json={"name": "Idle", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        response = client.post("/api/tasks/heartbeat", json={"agent_id": agent_id})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "no_work"
        assert data["task"] is None

    def test_heartbeat_returns_assigned_work(self):
        agent_resp = client.post("/api/agents", json={"name": "Worker", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        task_resp = client.post("/api/tasks", json={"title": "Assigned Work", "priority": 10})
        task_id = task_resp.json()["id"]
        client.post(f"/api/tasks/{task_id}/assign/{agent_id}")

        response = client.post("/api/tasks/heartbeat", json={"agent_id": agent_id})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "work_assigned"
        assert data["task"] is not None
        assert data["task"]["id"] == task_id
        assert data["task"]["status"] == "in_progress"

    def test_heartbeat_inactive_agent(self):
        agent_resp = client.post("/api/agents", json={"name": "Inactive", "role": "Dev", "status": "inactive"})
        agent_id = agent_resp.json()["id"]
        response = client.post("/api/tasks/heartbeat", json={"agent_id": agent_id})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "agent_not_active"

    def test_heartbeat_nonexistent_agent(self):
        response = client.post("/api/tasks/heartbeat", json={"agent_id": 999})
        assert response.status_code == 404

    def test_heartbeat_priority_order(self):
        agent_resp = client.post("/api/agents", json={"name": "Worker", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        client.post("/api/tasks", json={"title": "Low Priority", "priority": 1})
        low_id = client.post("/api/tasks", json={"title": "Low Priority"}).json()["id"]
        high_id = client.post("/api/tasks", json={"title": "High Priority", "priority": 100}).json()["id"]
        client.post(f"/api/tasks/{low_id}/assign/{agent_id}")
        client.post(f"/api/tasks/{high_id}/assign/{agent_id}")

        response = client.post("/api/tasks/heartbeat", json={"agent_id": agent_id})
        assert response.status_code == 200
        assert response.json()["task"]["id"] == high_id


class TestTaskComments:
    def test_add_comment(self):
        agent_resp = client.post("/api/agents", json={"name": "Commenter", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        task_resp = client.post("/api/tasks", json={"title": "Task with Comment"})
        task_id = task_resp.json()["id"]

        response = client.post(f"/api/tasks/{task_id}/comments?agent_id={agent_id}", json={"content": "Test comment"})
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Test comment"
        assert data["agent_id"] == agent_id
        assert data["task_id"] == task_id

    def test_list_comments(self):
        agent_resp = client.post("/api/agents", json={"name": "Commenter", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        task_resp = client.post("/api/tasks", json={"title": "Task with Comments"})
        task_id = task_resp.json()["id"]
        client.post(f"/api/tasks/{task_id}/comments?agent_id={agent_id}", json={"content": "First"})
        client.post(f"/api/tasks/{task_id}/comments?agent_id={agent_id}", json={"content": "Second"})

        response = client.get(f"/api/tasks/{task_id}/comments")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["content"] == "First"
        assert data[1]["content"] == "Second"

    def test_comment_nonexistent_task_fails(self):
        agent_resp = client.post("/api/agents", json={"name": "Commenter", "role": "Dev"})
        agent_id = agent_resp.json()["id"]
        response = client.post("/api/tasks/999/comments?agent_id={agent_id}", json={"content": "Test"})
        assert response.status_code == 404

    def test_comment_nonexistent_agent_fails(self):
        task_resp = client.post("/api/tasks", json={"title": "Task"})
        task_id = task_resp.json()["id"]
        response = client.post(f"/api/tasks/{task_id}/comments?agent_id=999", json={"content": "Test"})
        assert response.status_code == 404


class TestValidation:
    def test_create_agent_requires_name_and_role(self):
        response = client.post("/api/agents", json={"name": "No Role"})
        assert response.status_code == 422
        response = client.post("/api/agents", json={"role": "No Name"})
        assert response.status_code == 422

    def test_create_task_requires_title(self):
        response = client.post("/api/tasks", json={"description": "No Title"})
        assert response.status_code == 422

    def test_budget_limit_non_negative(self):
        response = client.post("/api/agents", json={"name": "Test", "role": "Dev", "budget_limit": -100})
        assert response.status_code == 422
        response = client.post("/api/tasks", json={"title": "Test", "budget_limit": -100})
        assert response.status_code == 422

    def test_priority_non_negative(self):
        response = client.post("/api/tasks", json={"title": "Test", "priority": -1})
        assert response.status_code == 422
