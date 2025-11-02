import React, { useState } from 'react'
import { Search, Send } from 'lucide-react'
import EntryCard from './EntryCard'

function SearchPanel({ onSearch, results }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>Search Your Memories</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
          Ask natural questions like "Tell me about happy moments" or "What did I do last week?"
        </p>
        
        <form onSubmit={handleSubmit}>
          <div className="search-form">
            <input
              type="text"
              className="input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="What would you like to remember?"
            />
            <button type="submit" className="btn btn-primary">
              <Send />
              Search
            </button>
          </div>
        </form>
      </div>

      {results && (
        <>
          {results.summary && (
            <div className="card search-summary">
              <h3>Summary</h3>
              <p style={{ whiteSpace: 'pre-wrap' }}>{results.summary}</p>
            </div>
          )}

          {results.relevant_entries && results.relevant_entries.length > 0 && (
            <div>
              <h3 style={{ marginBottom: '1rem' }}>
                Found {results.count} relevant {results.count === 1 ? 'entry' : 'entries'}
              </h3>
              {results.relevant_entries.map(entry => (
                <EntryCard key={entry.id} entry={entry} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default SearchPanel




