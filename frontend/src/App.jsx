import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Plus, Search, Mic, Image, FileText, Calendar, Clock } from 'lucide-react'
import EntryList from './components/EntryList'
import EntryForm from './components/EntryForm'
import SearchPanel from './components/SearchPanel'
import './App.css'

const API_URL = '/api'

function App() {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [showSearch, setShowSearch] = useState(false)
  const [searchResults, setSearchResults] = useState(null)

  useEffect(() => {
    loadEntries()
  }, [])

  const loadEntries = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/entries`)
      setEntries(response.data)
    } catch (error) {
      console.error('Error loading entries:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleNewEntry = async (formData) => {
    try {
      setLoading(true)
      await axios.post(`${API_URL}/entries`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      await loadEntries()
      setShowForm(false)
    } catch (error) {
      console.error('Error creating entry:', error)
      alert('Failed to create entry')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (query) => {
    try {
      setLoading(true)
      const response = await axios.post(`${API_URL}/query`, { text: query, limit: 20 })
      setSearchResults(response.data)
    } catch (error) {
      console.error('Error searching:', error)
      alert('Search failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this entry?')) return
    
    try {
      setLoading(true)
      await axios.delete(`${API_URL}/entries/${id}`)
      await loadEntries()
    } catch (error) {
      console.error('Error deleting entry:', error)
      alert('Failed to delete entry')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>
            <Calendar className="icon" />
            Personal Semantic Diary
          </h1>
          <p className="subtitle">Your intelligent memory companion</p>
        </div>
      </header>

      <nav className="nav">
        <div className="container">
          <div className="nav-buttons">
            <button 
              className="btn btn-primary"
              onClick={() => { setShowForm(!showForm); setShowSearch(false) }}
            >
              <Plus />
              New Entry
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => { setShowSearch(!showSearch); setShowForm(false) }}
            >
              <Search />
              Search
            </button>
          </div>
        </div>
      </nav>

      <main className="container">
        {showForm && (
          <EntryForm onSubmit={handleNewEntry} onCancel={() => setShowForm(false)} />
        )}

        {showSearch && (
          <SearchPanel onSearch={handleSearch} results={searchResults} />
        )}

        {!showForm && !showSearch && (
          <>
            <div className="stats">
              <div className="stat-item">
                <FileText className="icon" />
                <span>{entries.length} Entries</span>
              </div>
            </div>
            
            {loading ? (
              <div className="loading">Loading...</div>
            ) : (
              <EntryList 
                entries={entries} 
                onDelete={handleDelete}
                onRefresh={loadEntries}
              />
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default App




