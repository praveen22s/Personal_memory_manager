import React from 'react'
import { format } from 'date-fns'
import { Trash2, Clock } from 'lucide-react'
import EntryCard from './EntryCard'

function EntryList({ entries, onDelete, onRefresh }) {
  if (entries.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <h2>No entries yet</h2>
        <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>
          Start by creating your first diary entry!
        </p>
      </div>
    )
  }

  return (
    <div className="entry-list">
      {entries.map(entry => (
        <EntryCard 
          key={entry.id} 
          entry={entry} 
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}

export default EntryList




