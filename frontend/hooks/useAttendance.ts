import { useState, useCallback } from 'react'
import { attendanceAPI, AttendanceRequest } from '../lib/api'

export function useAttendance() {
  const [submitting, setSubmitting] = useState(false)

  const submitAttendance = useCallback(async (request: AttendanceRequest) => {
    setSubmitting(true)
    try {
      await attendanceAPI.createAttendance(request)
      return { success: true }
    } catch (error) {
      console.error('Error submitting attendance:', error)
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' }
    } finally {
      setSubmitting(false)
    }
  }, [])

  return {
    submitting,
    submitAttendance,
  }
}