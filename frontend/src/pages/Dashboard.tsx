import { useEffect, useState } from 'react'
import { agentsApi, tasksApi } from '../api'
import type { Agent, Task, TaskStatus } from '../types'
import './Dashboard.css'

export default function Dashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

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

  const agentStatusColors: Record<Agent['status'], string> = {
    active: '#10b981',
    inactive: '#9ca3af',
    busy: '#f59e0b',
    error: '#ef4444',
  }

  useEffect(() => {
    async function fetchData() {
      try {
        const [agentsRes, tasksRes] = await Promise.all([
          agentsApi.list({ limit: 10 }),
          tasksApi.list({ limit: 10 }),
        ])
        setAgents(agentsRes.data)
        setTasks(tasksRes.data)
      } catch (err) {
        setError('Failed to load dashboard data')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const activeAgents = agents.filter((a) => a.status === 'active').length
  const busyAgents = agents.filter((a) => a.status === 'busy').length
  const pendingTasks = tasks.filter((t) => t.status === 'pending').length
  const inProgressTasks = tasks.filter((t) => t.status === 'in_progress').length

  if (loading) {
    return <div className="dashboard loading">Loading...</div>
  }

  if (error) {
    return <div className="dashboard error">{error}</div>
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h2>Dashboard</h2>
        <p className="subtitle">Overview of your agent workforce</p>
      </header>

      <div className="stats-grid">
        <StatCard title="Total Agents" value={agents.length} icon="👥" />
        <StatCard title="Active Agents" value={activeAgents} icon="✅" color="#10b981" />
        <StatCard title="Busy Agents" value={busyAgents} icon="⚡" color="#f59e0b" />
        <StatCard title="Total Tasks" value={tasks.length} icon="📋" />
        <StatCard title="Pending Tasks" value={pendingTasks} icon="⏳" color="#f59e0b" />
        <StatCard title="In Progress" value={inProgressTasks} icon="🔄" color="#3b82f6" />
      </div>

      <div className="dashboard-sections">
        <section className="section">
          <h3>Recent Agents</h3>
          {agents.length === 0 ? (
            <p className="empty">No agents yet. <a href="/agents">Create your first agent</a></p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Budget Used</th>
                </tr>
              </thead>
              <tbody>
                {agents.slice(0, 5).map((agent) => (
                  <tr key={agent.id}>
                    <td>{agent.name}</td>
                    <td>{agent.role}</td>
                    <td>
                      <span
                        className="status-badge"
                        style={{ backgroundColor: agentStatusColors[agent.status] }}
                      >
                        {agent.status}
                      </span>
                    </td>
                    <td>${(agent.budget_used / 100).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>

        <section className="section">
          <h3>Recent Tasks</h3>
          {tasks.length === 0 ? (
            <p className="empty">No tasks yet. <a href="/tasks">Create your first task</a></p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Priority</th>
                  <th>Assignee</th>
                </tr>
              </thead>
              <tbody>
                {tasks.slice(0, 5).map((task) => (
                  <tr key={task.id}>
                    <td>{task.title}</td>
                    <td>
                      <span
                        className="status-badge"
                        style={{ backgroundColor: taskStatusColors[task.status] }}
                      >
                        {task.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td>{task.priority}</td>
                    <td>{task.assignee_id ? `Agent #${task.assignee_id}` : 'Unassigned'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </div>
    </div>
  )
}

function StatCard({ title, value, icon, color = '#4338ca' }: { title: string; value: number; icon: string; color?: string }) {
  return (
    <div className="stat-card">
      <div className="stat-icon" style={{ backgroundColor: color }}>
        {icon}
      </div>
      <div className="stat-info">
        <p className="stat-value">{value}</p>
        <p className="stat-title">{title}</p>
      </div>
    </div>
  )
}
