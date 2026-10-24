import { useEffect, useState } from 'react'
import { agentsApi } from '../api'
import type { Agent, AgentCreate, AgentUpdate, AgentStatus } from '../types'
import './Agents.css'

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [editingAgent, setEditingAgent] = useState<Agent | null>(null)
  const [formData, setFormData] = useState<AgentCreate>({
    name: '',
    role: '',
    description: '',
    model_provider: '',
    model_name: '',
    budget_limit: 0,
    parent_id: undefined,
  })

  const agentStatusColors: Record<AgentStatus, string> = {
    active: '#10b981',
    inactive: '#9ca3af',
    busy: '#f59e0b',
    error: '#ef4444',
  }

  useEffect(() => {
    fetchAgents()
  }, [])

  async function fetchAgents() {
    try {
      const res = await agentsApi.list({ limit: 100 })
      setAgents(res.data)
    } catch (err) {
      setError('Failed to load agents')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    try {
      if (editingAgent) {
        await agentsApi.update(editingAgent.id, formData)
      } else {
        await agentsApi.create(formData)
      }
      setShowForm(false)
      setEditingAgent(null)
      resetForm()
      fetchAgents()
    } catch (err) {
      setError('Failed to save agent')
      console.error(err)
    }
  }

  function handleEdit(agent: Agent) {
    setEditingAgent(agent)
    setFormData({
      name: agent.name,
      role: agent.role,
      description: agent.description || '',
      model_provider: agent.model_provider || '',
      model_name: agent.model_name || '',
      budget_limit: agent.budget_limit,
      parent_id: agent.parent_id || undefined,
    })
    setShowForm(true)
  }

  async function handleDelete(id: number) {
    if (!confirm('Delete this agent?')) return
    try {
      await agentsApi.delete(id)
      fetchAgents()
    } catch (err) {
      setError('Failed to delete agent')
      console.error(err)
    }
  }

  function resetForm() {
    setFormData({
      name: '',
      role: '',
      description: '',
      model_provider: '',
      model_name: '',
      budget_limit: 0,
      parent_id: undefined,
    })
  }

  function handleCancel() {
    setShowForm(false)
    setEditingAgent(null)
    resetForm()
  }

  if (loading) return <div className="page loading">Loading...</div>
  if (error) return <div className="page error">{error}</div>

  return (
    <div className="page agents-page">
      <header className="page-header">
        <h2>Agents</h2>
        <button className="btn btn-primary" onClick={() => { setEditingAgent(null); resetForm(); setShowForm(true); }}>
          + New Agent
        </button>
      </header>

      {showForm && (
        <div className="modal-overlay" onClick={handleCancel}>
          <form className="modal" onClick={(e) => e.stopPropagation()} onSubmit={handleSubmit}>
            <h3>{editingAgent ? 'Edit Agent' : 'New Agent'}</h3>
            <div className="form-group">
              <label htmlFor="name">Name *</label>
              <input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="role">Role *</label>
              <input
                id="role"
                type="text"
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
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
                <label htmlFor="model_provider">Model Provider</label>
                <input
                  id="model_provider"
                  type="text"
                  value={formData.model_provider}
                  onChange={(e) => setFormData({ ...formData, model_provider: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label htmlFor="model_name">Model Name</label>
                <input
                  id="model_name"
                  type="text"
                  value={formData.model_name}
                  onChange={(e) => setFormData({ ...formData, model_name: e.target.value })}
                />
              </div>
            </div>
            <div className="form-row">
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
              <div className="form-group">
                <label htmlFor="parent_id">Parent Agent ID</label>
                <input
                  id="parent_id"
                  type="number"
                  value={formData.parent_id || ''}
                  onChange={(e) => setFormData({ ...formData, parent_id: e.target.value ? parseInt(e.target.value) : undefined })}
                  min="1"
                />
              </div>
            </div>
            <div className="modal-actions">
              <button type="button" className="btn btn-secondary" onClick={handleCancel}>Cancel</button>
              <button type="submit" className="btn btn-primary">{editingAgent ? 'Update' : 'Create'}</button>
            </div>
          </form>
        </div>
      )}

      {agents.length === 0 ? (
        <div className="empty-state">
          <p>No agents yet. Click "New Agent" to create your first agent.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Status</th>
                <th>Model</th>
                <th>Budget</th>
                <th>Parent</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {agents.map((agent) => (
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
                  <td>
                    {agent.model_provider && agent.model_name
                      ? `${agent.model_provider}/${agent.model_name}`
                      : agent.model_provider || agent.model_name || '-'}
                  </td>
                  <td>${(agent.budget_used / 100).toFixed(2)} / ${(agent.budget_limit / 100).toFixed(2)}</td>
                  <td>{agent.parent_id ? `Agent #${agent.parent_id}` : '-'}</td>
                  <td className="actions">
                    <button className="btn btn-sm btn-secondary" onClick={() => handleEdit(agent)}>Edit</button>
                    <button className="btn btn-sm btn-danger" onClick={() => handleDelete(agent.id)}>Delete</button>
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
