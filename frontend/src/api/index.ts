import api from './client'
import type { Agent, AgentCreate, AgentUpdate, Task, TaskCreate, TaskUpdate, TaskComment, TaskCommentCreate, HeartbeatResponse, AgentStatus, TaskStatus } from '../types'

export const agentsApi = {
  list: (params?: { skip?: number; limit?: number; status?: AgentStatus }) =>
    api.get<Agent[]>('/agents', { params }),
  get: (id: number) => api.get<Agent>(`/agents/${id}`),
  create: (data: AgentCreate) => api.post<Agent>('/agents', data),
  update: (id: number, data: AgentUpdate) => api.patch<Agent>(`/agents/${id}`, data),
  delete: (id: number) => api.delete(`/agents/${id}`),
}

export const tasksApi = {
  list: (params?: { skip?: number; limit?: number; status?: TaskStatus; assignee_id?: number }) =>
    api.get<Task[]>('/tasks', { params }),
  get: (id: number) => api.get<Task>(`/tasks/${id}`),
  create: (data: TaskCreate) => api.post<Task>('/tasks', data),
  update: (id: number, data: TaskUpdate) => api.patch<Task>(`/tasks/${id}`, data),
  delete: (id: number) => api.delete(`/tasks/${id}`),
  assign: (taskId: number, agentId: number) => api.post<Task>(`/tasks/${taskId}/assign/${agentId}`),
  heartbeat: (agentId: number) => api.post<HeartbeatResponse>('/tasks/heartbeat', { agent_id: agentId }),
  addComment: (taskId: number, data: TaskCommentCreate, agentId: number) =>
    api.post<TaskComment>(`/tasks/${taskId}/comments`, data, { params: { agent_id: agentId } }),
  listComments: (taskId: number) => api.get<TaskComment[]>(`/tasks/${taskId}/comments`),
}
