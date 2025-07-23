import { useState, useEffect } from 'react'
import { attendanceAPI, AttendanceLog, User, UserStatus } from '../lib/api'

export function useAttendanceData() {
  const [logs, setLogs] = useState<AttendanceLog[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [usersStatus, setUsersStatus] = useState<UserStatus[]>([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      const [logsResponse, usersResponse, statusResponse] = await Promise.all([
        attendanceAPI.getAttendanceLogs(),
        attendanceAPI.getUsers(),
        attendanceAPI.getUsersStatus(),
      ])

      setLogs(logsResponse.data || [])
      setUsers(usersResponse.data || [])
      setUsersStatus(statusResponse.data || [])
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const refreshData = async () => {
    try {
      const [logsResponse, statusResponse] = await Promise.all([
        attendanceAPI.getAttendanceLogs(),
        attendanceAPI.getUsersStatus(),
      ])

      setLogs(logsResponse.data || [])
      setUsersStatus(statusResponse.data || [])
    } catch (error) {
      console.error('Failed to refresh data:', error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return {
    logs,
    users,
    usersStatus,
    loading,
    refreshData,
  }
}