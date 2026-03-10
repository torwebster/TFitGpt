'use client'
import { useState } from 'react'

export default function Onboarding() {
  const [userId, setUserId] = useState('1')
  const [status, setStatus] = useState('')

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = new FormData(e.currentTarget)
    const payload = {
      goals: [form.get('goal')],
      injuries: String(form.get('injuries') || '').split(',').map(s => s.trim()).filter(Boolean),
      equipment: String(form.get('equipment') || '').split(',').map(s => s.trim()).filter(Boolean),
      schedule: { today_minutes: Number(form.get('minutes') || 45) },
      preferences: { style: form.get('style') }
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/profile/${userId}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    setStatus(res.ok ? 'Saved onboarding profile.' : 'Failed to save profile')
  }

  return (
    <form className="card" onSubmit={submit}>
      <h2>Onboarding</h2>
      <label>User ID<input value={userId} onChange={e => setUserId(e.target.value)} /></label>
      <label>Goal<input name="goal" defaultValue="fat_loss" /></label>
      <label>Injuries (comma separated)<input name="injuries" defaultValue="achilles" /></label>
      <label>Equipment (comma separated)<input name="equipment" defaultValue="dumbbells" /></label>
      <label>Time available today (mins)<input name="minutes" defaultValue="30" /></label>
      <label>Coaching style<input name="style" defaultValue="direct" /></label>
      <button type="submit">Save</button>
      <p>{status}</p>
    </form>
  )
}
