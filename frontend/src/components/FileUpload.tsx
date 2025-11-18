import React, { useState, useRef } from 'react';
import { validateFile } from '../utils/validators';

interface FileUploadProps {
  onUpload: (file: File, type: 'video' | 'audio' | 'image') => void;
  uploading: boolean;
  progress: number;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUpload, uploading, progress }) => {
  const [uploadType, setUploadType] = useState<'video' | 'audio' | 'image'>('video');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string>('');
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (file: File) => {
    setError('');
    const validation = validateFile(file, uploadType);

    if (!validation.valid) {
      setError(validation.message || 'Invalid file');
      return;
    }

    setSelectedFile(file);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile, uploadType);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload-container">
      <div className="upload-type-selector">
        <button
          className={`type-btn ${uploadType === 'video' ? 'active' : ''}`}
          onClick={() => setUploadType('video')}
          disabled={uploading}
        >
          Video
        </button>
        <button
          className={`type-btn ${uploadType === 'audio' ? 'active' : ''}`}
          onClick={() => setUploadType('audio')}
          disabled={uploading}
        >
          Audio
        </button>
        <button
          className={`type-btn ${uploadType === 'image' ? 'active' : ''}`}
          onClick={() => setUploadType('image')}
          disabled={uploading}
        >
          Image
        </button>
      </div>

      <div
        className={`dropzone ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleBrowseClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileChange}
          accept={
            uploadType === 'video'
              ? 'video/*'
              : uploadType === 'audio'
              ? 'audio/*'
              : 'image/*'
          }
          style={{ display: 'none' }}
        />
        <div className="dropzone-content">
          {selectedFile ? (
            <>
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </>
          ) : (
            <>
              <p>Drag & drop your {uploadType} file here</p>
              <p className="or-text">or</p>
              <button className="btn-browse" type="button">
                Browse Files
              </button>
            </>
          )}
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}

      {uploading && (
        <div className="upload-progress">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
          </div>
          <p>{progress}% uploaded</p>
        </div>
      )}

      {selectedFile && !uploading && (
        <button className="btn-upload" onClick={handleUpload}>
          Upload and Fact Check
        </button>
      )}
    </div>
  );
};

export default FileUpload;
