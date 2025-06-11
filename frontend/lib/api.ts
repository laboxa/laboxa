const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface AttendanceLog {
  id: number
  user_name: string
  type: 'checkin' | 'checkout'
  timestamp: string
}

export interface User {
  id: number
  name: string
}

export interface UserStatus {
  id: number
  name: string
  status: 'checkin' | 'checkout'
  last_action_time: string | null
}

export interface AttendanceRequest {
  user_name: string
  type: 'checkin' | 'checkout'
}

class AttendanceAPI {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    return response.json()
  }

  async getAttendanceLogs(): Promise<{ data: AttendanceLog[] }> {
    return this.request('/api/attendance')
  }

  async getUsers(): Promise<{ data: User[] }> {
    return this.request('/api/users')
  }

  async getUsersStatus(): Promise<{ data: UserStatus[] }> {
    return this.request('/api/users/status')
  }

  async createAttendance(request: AttendanceRequest): Promise<{ message: string }> {
    return this.request('/api/attendance', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }
}

export const attendanceAPI = new AttendanceAPI()