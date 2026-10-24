import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../App'

const renderApp = () => render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)

describe('App', () => {
  it('renders dashboard by default', () => {
    renderApp()
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })

  it('has navigation links', () => {
    renderApp()
    expect(screen.getByRole('link', { name: /agents/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /tasks/i })).toBeInTheDocument()
  })

  it('navigates to agents page', () => {
    renderApp()
    fireEvent.click(screen.getByRole('link', { name: /agents/i }))
    expect(screen.getByText('Agents')).toBeInTheDocument()
  })

  it('navigates to tasks page', () => {
    renderApp()
    fireEvent.click(screen.getByRole('link', { name: /tasks/i }))
    expect(screen.getByText('Tasks')).toBeInTheDocument()
  })
})
