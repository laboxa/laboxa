// Next.js API Routesを経由してバックエンドにアクセス
const API_BASE_URL = '/api' // Next.js内部のAPI Routes

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
    return this.request('/attendance')
  }

  async getUsers(): Promise<{ data: User[] }> {
    return this.request('/users')
  }

  async getUsersStatus(): Promise<{ data: UserStatus[] }> {
    return this.request('/users/status')
  }

  async createAttendance(request: AttendanceRequest): Promise<{ message: string }> {
    return this.request('/attendance', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }
}

export const attendanceAPI = new AttendanceAPI()