export type AgentStatus = 'active' | 'inactive' | 'busy' | 'error'
export type TaskStatus = 'pending' | 'assigned' | 'in_progress' | 'in_review' | 'approved' | 'rejected' | 'completed' | 'failed'

export interface Agent {
  id: number
  name: string
  role: string
  description: string | null
  status: AgentStatus
  model_provider: string | null
  model_name: string | null
  budget_limit: number
  budget_used: number
  parent_id: number | null
  created_at: string
  updated_at: string
}

export interface AgentCreate {
  name: string
  role: string
  description?: string
  model_provider?: string
  model_name?: string
  budget_limit?: number
  parent_id?: number
}

export interface AgentUpdate {
  name?: string
  role?: string
  description?: string
  status?: AgentStatus
  model_provider?: string
  model_name?: string
  budget_limit?: number
  parent_id?: number
}

export interface Task {
  id: number
  title: string
  description: string | null
  status: TaskStatus
  priority: number
  assignee_id: number | null
  creator_id: number | null
  parent_task_id: number | null
  budget_limit: number
  budget_used: number
  created_at: string
  updated_at: string
  completed_at: string | null
}

export interface TaskCreate {
  title: string
  description?: string
  priority?: number
  budget_limit?: number
  parent_task_id?: number
}

export interface TaskUpdate {
  title?: string
  description?: string
  status?: TaskStatus
  priority?: number
  assignee_id?: number
  budget_limit?: number
  parent_task_id?: number
}

export interface TaskComment {
  id: number
  task_id: number
  agent_id: number
  content: string
  created_at: string
}

export interface TaskCommentCreate {
  content: string
}

export interface HeartbeatResponse {
  task: Task | null
  message: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}
