import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import HistoryItem from '../components/HistoryItem';
import ResultCard from '../components/ResultCard';
import CommentBox from '../components/CommentBox';
import LoadingSpinner from '../components/LoadingSpinner';
import * as factCheckService from '../services/factCheckService';
import { FactCheck } from '../types/factCheck';

const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<FactCheck[]>([]);
  const [selectedFactCheck, setSelectedFactCheck] = useState<FactCheck | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await factCheckService.getUserHistory();
      setHistory(data);
    } catch (err: any) {
      setError(err.detail || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const handleItemClick = async (factCheck: FactCheck) => {
    try {
      const details = await factCheckService.getFactCheckDetails(factCheck.fact_check_id);
      setSelectedFactCheck(details);
    } catch (err: any) {
      setError(err.detail || 'Failed to load details');
    }
  };

  const handleBackToList = () => {
    setSelectedFactCheck(null);
  };

  if (loading) {
    return (
      <div className="history-page">
        <Navbar />
        <LoadingSpinner message="Loading history..." />
      </div>
    );
  }

  return (
    <div className="history-page">
      <Navbar />
      <div className="history-container">
        {!selectedFactCheck ? (
          <>
            <div className="history-header">
              <h2>Your Fact-Check History</h2>
              <p>{history.length} total fact-checks</p>
            </div>

            {error && <div className="error-message">{error}</div>}

            {history.length === 0 ? (
              <div className="empty-state">
                <p>No fact-checks yet. Upload some content to get started!</p>
              </div>
            ) : (
              <div className="history-list">
                {history.map((factCheck) => (
                  <HistoryItem
                    key={factCheck.fact_check_id}
                    factCheck={factCheck}
                    onClick={() => handleItemClick(factCheck)}
                  />
                ))}
              </div>
            )}
          </>
        ) : (
          <>
            <button className="btn-back" onClick={handleBackToList}>
              ← Back to History
            </button>

            <ResultCard
              extractedText={selectedFactCheck.extracted_text}
              response={selectedFactCheck.gemini_response}
              citations={selectedFactCheck.citations}
            />

            <CommentBox comments={selectedFactCheck.admin_comments || []} />
          </>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
