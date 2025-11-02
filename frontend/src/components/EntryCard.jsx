import React from 'react'
import { format } from 'date-fns'
import { Trash2, Clock, Image, Mic } from 'lucide-react'

function EntryCard({ entry, onDelete }) {
  const hasMedia = entry.image_path || entry.audio_path

  return (
    <div className="card entry-card">
      <div className="entry-header">
        <h3>{entry.title}</h3>
        {onDelete && (
          <button 
            className="btn btn-danger"
            style={{ padding: '0.5rem' }}
            onClick={() => onDelete(entry.id)}
          >
            <Trash2 size={16} />
          </button>
        )}
      </div>

      {entry.tags && entry.tags.length > 0 && (
        <div className="entry-tags">
          {entry.tags.map((tag, idx) => (
            <span key={idx} className="tag">{tag}</span>
          ))}
        </div>
      )}

      {entry.text && (
        <p className="entry-text">{entry.text}</p>
      )}

      {hasMedia && (
        <div className="entry-media">
          {entry.image_path && (
            <div className="media-item">
              <Image size={20} />
              <img 
                src={`http://localhost:8000/${entry.image_path}`} 
                alt="Entry image"
                style={{ maxWidth: '200px', borderRadius: '0.5rem', marginTop: '0.5rem' }}
              />
            </div>
          )}
          
          {entry.audio_path && (
            <div className="media-item">
              <Mic size={20} />
              <audio 
                controls 
                src={`http://localhost:8000/${entry.audio_path}`}
                style={{ marginTop: '0.5rem', width: '100%' }}
              />
            </div>
          )}
        </div>
      )}

      <div className="entry-footer">
        <Clock size={14} />
        <span>{format(new Date(entry.timestamp), 'PPp')}</span>
        {entry.similarity_score && (
          <span className="similarity">
            Match: {(entry.similarity_score * 100).toFixed(1)}%
          </span>
        )}
      </div>
    </div>
  )
}

export default EntryCard
