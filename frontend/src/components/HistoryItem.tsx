import React from 'react';
import { FactCheck } from '../types/factCheck';
import { formatDate, truncateText } from '../utils/formatters';

interface HistoryItemProps {
  factCheck: FactCheck;
  onClick: () => void;
}

const HistoryItem: React.FC<HistoryItemProps> = ({ factCheck, onClick }) => {
  const hasComments = factCheck.admin_comments && factCheck.admin_comments.length > 0;

  return (
    <div className="history-item" onClick={onClick}>
      <div className="history-header">
        <span className="upload-type-badge">{factCheck.upload_type}</span>
        <span className="timestamp">{formatDate(factCheck.timestamp)}</span>
      </div>
      <div className="history-content">
        <p className="response-preview">{truncateText(factCheck.gemini_response, 150)}</p>
      </div>
      <div className="history-footer">
        {hasComments && (
          <span className="comment-indicator">
            {factCheck.admin_comments.length} admin comment(s)
          </span>
        )}
        <span className="view-details">View Details →</span>
      </div>
    </div>
  );
};

export default HistoryItem;
