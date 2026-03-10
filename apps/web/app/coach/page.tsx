'use client'
import { useState } from 'react'

export default function CoachPage() {
  const [text, setText] = useState('pain: achilles 6/10 and I can only do 30 mins')
  const [userId, setUserId] = useState('1')
  const [reply, setReply] = useState<any>(null)

  async function send() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/coach/message`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ user_id: Number(userId), text, attachments: [], channel: 'web' })
    })
    setReply(await res.json())
  }

  return (
    <div>
      <div className="card">
        <h2>Ask Coach</h2>
        <input value={userId} onChange={e => setUserId(e.target.value)} />
        <textarea value={text} onChange={e => setText(e.target.value)} rows={4} />
        <button onClick={send}>Send</button>
      </div>
      {reply && <div className="card"><p><b>Intent:</b> {reply.intent.intent}</p><p>{reply.response.message}</p></div>}
      <a className="fab" href="/coach"><button>Coach</button></a>
    </div>
  )
}
