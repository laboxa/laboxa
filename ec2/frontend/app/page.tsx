'use client'

import { useAttendanceData } from '../hooks/useAttendanceData'
import { useAttendance } from '../hooks/useAttendance'
import QuickAttendance from '../components/AttendanceStatusPanel'
import AttendanceTable from '../components/AttendanceTable'

export default function Home() {
  const { logs, users, usersStatus, loading, refreshData } = useAttendanceData()
  const { submitting, submitAttendance } = useAttendance()

  const handleQuickToggle = async (userName: string, nextAction: 'checkin' | 'checkout') => {
    const result = await submitAttendance({
      user_name: userName,
      type: nextAction,
    })

    if (result.success) {
      await refreshData()
    } else {
      alert('Failed to record attendance')
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-8">
        Attendance Management System
      </h1>
      
      <QuickAttendance 
        users={users}
        usersStatus={usersStatus}
        onToggle={handleQuickToggle}
        submitting={submitting}
      />
      
      <AttendanceTable logs={logs} />
    </div>
  )
}