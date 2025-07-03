interface AttendanceLog {
  id: number
  user_name: string
  type: 'checkin' | 'checkout'
  timestamp: string
}

interface AttendanceTableProps {
  logs: AttendanceLog[]
}

export default function AttendanceTable({ logs }: AttendanceTableProps) {
  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('ja-JP')
  }

  return (
    <div className="bg-white border rounded-lg">
      <div className="px-4 py-3 border-b">
        <h2 className="text-lg font-medium">Attendance Records</h2>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b bg-gray-50">
              <th className="px-4 py-2 text-left text-sm font-medium">ID</th>
              <th className="px-4 py-2 text-left text-sm font-medium">Name</th>
              <th className="px-4 py-2 text-left text-sm font-medium">Type</th>
              <th className="px-4 py-2 text-left text-sm font-medium">Time</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className="border-b last:border-b-0">
                <td className="px-4 py-2 text-sm">{log.id}</td>
                <td className="px-4 py-2 text-sm font-medium">{log.user_name}</td>
                <td className="px-4 py-2 text-sm">
                  <span className={`px-2 py-1 text-xs rounded ${
                    log.type === 'checkin' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {log.type === 'checkin' ? 'Check In' : 'Check Out'}
                  </span>
                </td>
                <td className="px-4 py-2 text-sm">{formatTimestamp(log.timestamp)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {logs.length === 0 && (
        <div className="text-center py-8 text-gray-500 text-sm">
          No records found
        </div>
      )}
    </div>
  )
}