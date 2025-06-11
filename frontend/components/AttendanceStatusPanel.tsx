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
      return 'bg-green-600 hover:bg-green-700 text-white border-green-600'
    } else {
      return 'bg-red-600 hover:bg-red-700 text-white border-red-600'
    }
  }

  const getButtonText = (userName: string) => {
    const nextAction = getNextAction(userName)
    
    if (nextAction === 'checkin') {
      return '🟢 Check In'
    } else {
      return '🔴 Check Out'
    }
  }

  return (
    <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4">Attendance Status</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {users.map((user) => {
          const currentStatus = getUserStatus(user.name)
          const nextAction = getNextAction(user.name)
          const lastActionTime = getLastActionTime(user.name)
          
          return (
            <div
              key={user.id}
              className={`p-4 rounded-lg border-2 transition-all ${
                currentStatus === 'checkin'
                  ? 'border-green-500 bg-green-50'
                  : 'border-red-500 bg-red-50'
              }`}
            >
              <div className="flex flex-col space-y-3">
                {/* ユーザー名とステータス */}
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-800">{user.name}</h3>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      currentStatus === 'checkin'
                        ? 'bg-green-200 text-green-800'
                        : 'bg-red-200 text-red-800'
                    }`}
                  >
                    {currentStatus === 'checkin' ? 'IN' : 'OUT'}
                  </span>
                </div>

                {/* 最後のアクション時刻 */}
                {lastActionTime && (
                  <p className="text-sm text-gray-600">
                    Last: {new Date(lastActionTime).toLocaleString('ja-JP')}
                  </p>
                )}

                {/* ワンタップボタン */}
                <button
                  onClick={() => onToggle(user.name, nextAction)}
                  disabled={submitting}
                  className={`w-full px-4 py-2 rounded-md font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${getButtonStyle(user.name)}`}
                >
                  {submitting ? 'Processing...' : getButtonText(user.name)}
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}