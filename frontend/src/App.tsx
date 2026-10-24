import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Tasks from './pages/Tasks'
import Layout from './components/Layout'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/tasks" element={<Tasks />} />
      </Routes>
    </Layout>
  )
}

export default App
