import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { fetchDashboardData } from '../api/clickup'
import Layout from '../components/dashboard/Layout'
import StatsGrid from '../components/dashboard/StatsGrid'
import ProductivityChart from '../components/charts/ProductivityChart'
import TasksTable from '../components/dashboard/TasksTable'

export default function Dashboard() {
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true)
        const result = await fetchDashboardData()
        setData(result)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    
    if (user) loadData()
  }, [user])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <Layout>
      <StatsGrid metrics={data.metrics} />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <ProductivityChart data={data.productivity} />
        <TasksTable tasks={data.recentTasks} />
      </div>
    </Layout>
  )
}