import { useEffect, useState } from 'react'
import { tasksApi, agentsApi } from '../api'
import type { Task, TaskCreate, TaskStatus, Agent } from '../types'
import './Tasks.css'

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: '',
    priority: 0,
    budget_limit: 0,
    parent_task_id: undefined,
  })

  const taskStatusColors: Record<TaskStatus, string> = {
    pending: '#f59e0b',
    assigned: '#3b82f6',
    in_progress: '#8b5cf6',
    in_review: '#06b6d4',
    approved: '#22c55e',
    rejected: '#ef4444',
    completed: '#10b981',
    failed: '#dc2626',
  }

  const statusOrder: TaskStatus[] = [
    'pending', 'assigned', 'in_progress', 'in_review', 'approved', 'rejected', 'completed', 'failed'
  ]

  useEffect(() => {
    fetchData()
  }, [])

  async function fetchData() {
    try {
      const [tasksRes, agentsRes] = await Promise.all([
        tasksApi.list({ limit: 100 }),
        agentsApi.list({ limit: 100 }),
      ])
      setTasks(tasksRes.data)
      setAgents(agentsRes.data)
    } catch (err) {
      setError('Failed to load data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    try {
      if (editingTask) {
        await tasksApi.update(editingTask.id, formData)
      } else {
        await tasksApi.create(formData)
      }
      setShowForm(false)
      setEditingTask(null)
      resetForm()
      fetchData()
    } catch (err) {
      setError('Failed to save task')
      console.error(err)
    }
  }

  function handleEdit(task: Task) {
    setEditingTask(task)
    setFormData({
      title: task.title,
      description: task.description || '',
      priority: task.priority,
      budget_limit: task.budget_limit,
      parent_task_id: task.parent_task_id || undefined,
    })
    setShowForm(true)
  }

  async function handleDelete(id: number) {
    if (!confirm('Delete this task?')) return
    try {
      await tasksApi.delete(id)
      fetchData()
    } catch (err) {
      setError('Failed to delete task')
      console.error(err)
    }
  }

  async function handleAssign(taskId: number, agentId: number) {
    try {
      await tasksApi.assign(taskId, agentId)
      fetchData()
    } catch (err) {
      setError('Failed to assign task')
      console.error(err)
    }
  }

  function resetForm() {
    setFormData({
      title: '',
      description: '',
      priority: 0,
      budget_limit: 0,
      parent_task_id: undefined,
    })
  }

  function handleCancel() {
    setShowForm(false)
    setEditingTask(null)
    resetForm()
  }

  if (loading) return <div className="page loading">Loading...</div>
  if (error) return <div className="page error">{error}</div>

  const sortedTasks = [...tasks].sort((a, b) => statusOrder.indexOf(a.status) - statusOrder.indexOf(b.status))

  return (
    <div className="page tasks-page">
      <header className="page-header">
        <h2>Tasks</h2>
        <button className="btn btn-primary" onClick={() => { setEditingTask(null); resetForm(); setShowForm(true); }}>
          + New Task
        </button>
      </header>

      {showForm && (
        <div className="modal-overlay" onClick={handleCancel}>
          <form className="modal" onClick={(e) => e.stopPropagation()} onSubmit={handleSubmit}>
            <h3>{editingTask ? 'Edit Task' : 'New Task'}</h3>
            <div className="form-group">
              <label htmlFor="title">Title *</label>
              <input
                id="title"
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="priority">Priority</label>
                <input
                  id="priority"
                  type="number"
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: parseInt(e.target.value) || 0 })}
                  min="0"
                />
              </div>
              <div className="form-group">
                <label htmlFor="budget_limit">Budget Limit (cents)</label>
                <input
                  id="budget_limit"
                  type="number"
                  value={formData.budget_limit}
                  onChange={(e) => setFormData({ ...formData, budget_limit: parseInt(e.target.value) || 0 })}
                  min="0"
                />
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="parent_task_id">Parent Task ID</label>
              <input
                id="parent_task_id"
                type="number"
                value={formData.parent_task_id || ''}
                onChange={(e) => setFormData({ ...formData, parent_task_id: e.target.value ? parseInt(e.target.value) : undefined })}
                min="1"
              />
            </div>
            <div className="modal-actions">
              <button type="button" className="btn btn-secondary" onClick={handleCancel}>Cancel</button>
              <button type="submit" className="btn btn-primary">{editingTask ? 'Update' : 'Create'}</button>
            </div>
          </form>
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="empty-state">
          <p>No tasks yet. Click "New Task" to create your first task.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Assignee</th>
                <th>Budget</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sortedTasks.map((task) => (
                <tr key={task.id}>
                  <td>
                    <div className="task-title">
                      <span>{task.title}</span>
                      {task.description && <span className="task-desc">{task.description}</span>}
                    </div>
                  </td>
                  <td>
                    <span
                      className="status-badge"
                      style={{ backgroundColor: taskStatusColors[task.status] }}
                    >
                      {task.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td>{task.priority}</td>
                  <td>
                    {task.assignee_id
                      ? agents.find(a => a.id === task.assignee_id)?.name || `Agent #${task.assignee_id}`
                      : (
                        <select
                          value=""
                          onChange={(e) => e.target.value && handleAssign(task.id, parseInt(e.target.value))}
                          className="assign-select"
                        >
                          <option value="">Assign...</option>
                          {agents.filter(a => a.status === 'active').map((agent) => (
                            <option key={agent.id} value={agent.id}>{agent.name} ({agent.role})</option>
                          ))}
                        </select>
                      )}
                  </td>
                  <td>${(task.budget_used / 100).toFixed(2)} / ${(task.budget_limit / 100).toFixed(2)}</td>
                  <td className="actions">
                    <button className="btn btn-sm btn-secondary" onClick={() => handleEdit(task)}>Edit</button>
                    <button className="btn btn-sm btn-danger" onClick={() => handleDelete(task.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
