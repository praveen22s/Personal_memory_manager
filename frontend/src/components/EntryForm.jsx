import React, { useState } from 'react'
import { Mic, Image, FileText, X } from 'lucide-react'

function EntryForm({ onSubmit, onCancel }) {
  const [title, setTitle] = useState('')
  const [text, setText] = useState('')
  const [audioFile, setAudioFile] = useState(null)
  const [imageFile, setImageFile] = useState(null)
  const [tags, setTags] = useState('')
  const [recording, setRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()

    const formData = new FormData()
    formData.append('title', title || 'Untitled')
    if (text) formData.append('text', text)
    if (audioFile) formData.append('audio', audioFile)
    if (imageFile) formData.append('image', imageFile)
    if (tags) formData.append('tags', tags)

    onSubmit(formData)
    
    // Reset form
    setTitle('')
    setText('')
    setAudioFile(null)
    setImageFile(null)
    setTags('')
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)
      const chunks = []

      recorder.ondataavailable = (e) => chunks.push(e.data)
      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' })
        setAudioFile(blob)
      }

      recorder.start()
      setMediaRecorder(recorder)
      setRecording(true)
    } catch (error) {
      console.error('Error starting recording:', error)
      alert('Microphone access denied')
    }
  }

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop()
      mediaRecorder.stream.getTracks().forEach(track => track.stop())
      setMediaRecorder(null)
      setRecording(false)
    }
  }

  return (
    <div className="card">
      <div className="form-header">
        <h2>New Entry</h2>
        <button className="btn btn-secondary" style={{ padding: '0.5rem' }} onClick={onCancel}>
          <X size={20} />
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            className="input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Give your entry a title..."
          />
        </div>

        <div className="form-group">
          <label>Text</label>
          <textarea
            className="input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write your thoughts..."
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Tags (comma-separated)</label>
            <input
              type="text"
              className="input"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="happy, work, family..."
            />
          </div>
        </div>

        <div className="form-actions">
          <label className="file-label">
            <Image />
            {imageFile ? imageFile.name : 'Upload Image'}
            <input
              type="file"
              className="file-input"
              accept="image/*"
              onChange={(e) => setImageFile(e.target.files[0])}
            />
          </label>

          {!recording ? (
            <button type="button" className="btn btn-secondary" onClick={startRecording}>
              <Mic />
              Record Audio
            </button>
          ) : (
            <button type="button" className="btn btn-danger" onClick={stopRecording}>
              <Mic />
              Stop Recording
            </button>
          )}
        </div>

        {audioFile && !recording && (
          <div style={{ marginTop: '1rem', color: 'var(--success)' }}>
            ✓ Audio ready to upload
          </div>
        )}

        <div className="form-footer">
          <button type="button" className="btn btn-secondary" onClick={onCancel}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary">
            <FileText />
            Save Entry
          </button>
        </div>
      </form>
    </div>
  )
}

export default EntryForm




