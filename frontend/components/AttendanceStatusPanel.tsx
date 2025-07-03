interface User {
  id: number
  name: string
}

interface UserStatus {
  id: number
  name: string
  status: 'checkin' | 'checkout'
  last_action_time: string | null
}

interface QuickAttendanceProps {
  users: User[]
  usersStatus: UserStatus[]
  onToggle: (userName: string, nextAction: 'checkin' | 'checkout') => void
  submitting: boolean
}

export default function QuickAttendance({ 
  users, 
  usersStatus, 
  onToggle, 
  submitting 
}: QuickAttendanceProps) {
  const getUserStatus = (userName: string): 'checkin' | 'checkout' => {
    const userStatus = usersStatus.find(u => u.name === userName)
    return userStatus?.status || 'checkout'
  }

  const getNextAction = (userName: string): 'checkin' | 'checkout' => {
    const currentStatus = getUserStatus(userName)
    return currentStatus === 'checkout' ? 'checkin' : 'checkout'
  }

  const getLastActionTime = (userName: string): string | null => {
    const userStatus = usersStatus.find(u => u.name === userName)
    return userStatus?.last_action_time || null
  }

  const getButtonStyle = (userName: string) => {
    const nextAction = getNextAction(userName)
    
    if (nextAction === 'checkin') {
      return 'bg-green-600 hover:bg-green-700 active:bg-green-800 text-white shadow-sm'
    } else {
      return 'bg-red-600 hover:bg-red-700 active:bg-red-800 text-white shadow-sm'
    }
  }

  const getButtonText = (userName: string) => {
    const nextAction = getNextAction(userName)
    
    if (nextAction === 'checkin') {
      return 'Check In'
    } else {
      return 'Check Out'
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold mb-6">Attendance Status</h2>
      <div className="space-y-4">
        {users.map((user) => {
          const currentStatus = getUserStatus(user.name)
          const nextAction = getNextAction(user.name)
          const lastActionTime = getLastActionTime(user.name)
          
          return (
            <div
              key={user.id}
              className="flex items-center justify-between p-4 rounded-lg border-2 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3">
                  <span className="text-lg font-semibold text-gray-900">{user.name}</span>
                  <span
                    className={`px-3 py-1 text-sm font-bold rounded-full ${
                      currentStatus === 'checkin'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {currentStatus === 'checkin' ? 'IN' : 'OUT'}
                  </span>
                </div>
                {lastActionTime && (
                  <span className="text-sm text-gray-500 ml-4">
                    Last: {new Date(lastActionTime).toLocaleString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                )}
              </div>
              
              <button
                onClick={() => onToggle(user.name, nextAction)}
                disabled={submitting}
                className={`px-6 py-3 text-base font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 active:scale-95 min-w-[120px] ${getButtonStyle(user.name)}`}
              >
                {submitting ? 'Loading...' : getButtonText(user.name)}
              </button>
            </div>
          )
        })}
      </div>
    </div>
  )
}