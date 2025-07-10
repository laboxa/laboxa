import type { NextApiRequest, NextApiResponse } from 'next'

const BACKEND_URL = process.env.BACKEND_API_URL || 'http://localhost:8000'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    let response: Response

    if (req.method === 'GET') {
      // GET /api/attendance
      response = await fetch(`${BACKEND_URL}/api/attendance`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    } else if (req.method === 'POST') {
      // POST /api/attendance
      response = await fetch(`${BACKEND_URL}/api/attendance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(req.body),
      })
    } else {
      return res.status(405).json({ message: 'Method not allowed' })
    }

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`)
    }

    const data = await response.json()
    res.status(200).json(data)
  } catch (error) {
    console.error('API Error:', error)
    res.status(500).json({ message: 'Internal server error', error: String(error) })
  }
}
