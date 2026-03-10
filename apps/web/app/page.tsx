import Link from 'next/link'

export default function Home() {
  return (
    <div className="card">
      <h2>AI Fitness OS</h2>
      <p>Sign in with Google (configured in NextAuth) then finish onboarding in under 3 mins.</p>
      <p><Link href="/onboarding">Start onboarding</Link></p>
    </div>
  )
}
