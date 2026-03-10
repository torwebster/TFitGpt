'use client'
import { useState } from 'react'

export default function TodayPage() {
  const [userId, setUserId] = useState('1')
  const [plan, setPlan] = useState<any>(null)

  async function loadPlan() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/today-plan`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ user_id: Number(userId) }) })
    setPlan(await res.json())
  }

  return (
    <div>
      <div className="card">
        <h2>Today Plan</h2>
        <input value={userId} onChange={e => setUserId(e.target.value)} />
        <button onClick={loadPlan}>Generate</button>
      </div>
      {plan && <div className="card"><p>Readiness: {plan.readiness}</p><ul>{plan.actions.map((a: string) => <li key={a}>{a}</li>)}</ul></div>}
    </div>
  )
}
