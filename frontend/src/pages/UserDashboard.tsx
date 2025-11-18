import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import FileUpload from '../components/FileUpload';
import ResultCard from '../components/ResultCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { useFileUpload } from '../hooks/useFileUpload';
import * as factCheckService from '../services/factCheckService';
import { FactCheckResult } from '../types/factCheck';

const UserDashboard: React.FC = () => {
  const [result, setResult] = useState<FactCheckResult | null>(null);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

  const { uploadFile, uploading, progress } = useFileUpload();
  const navigate = useNavigate();

  const handleUpload = async (file: File, type: 'video' | 'audio' | 'image') => {
    setError('');
    setResult(null);

    try {
      // Upload file
      const uploadResponse = await uploadFile(file, type);

      // Process fact-check
      setProcessing(true);
      const factCheckResult = await factCheckService.processFactCheck(
        uploadResponse.data.file_path,
        uploadResponse.data.upload_type
      );

      setResult(factCheckResult);
    } catch (err: any) {
      setError(err.detail || 'An error occurred during processing');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="user-dashboard">
      <Navbar />
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h2>Upload Content for Fact-Checking</h2>
          <p>Upload a video, audio, or image to verify its accuracy</p>
        </div>

        <FileUpload onUpload={handleUpload} uploading={uploading} progress={progress} />

        {error && <div className="error-message">{error}</div>}

        {processing && (
          <LoadingSpinner message="Processing your content. This may take a moment..." />
        )}

        {result && !processing && (
          <ResultCard
            extractedText={result.extracted_text}
            response={result.gemini_response}
            citations={result.citations}
          />
        )}
      </div>
    </div>
  );
};

export default UserDashboard;
