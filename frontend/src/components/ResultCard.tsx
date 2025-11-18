import React from 'react';
import { Citation } from '../types/factCheck';

interface ResultCardProps {
  extractedText?: string;
  response: string;
  citations: Citation[];
}

const ResultCard: React.FC<ResultCardProps> = ({ extractedText, response, citations }) => {
  return (
    <div className="result-card">
      <h3>Fact-Check Results</h3>

      {extractedText && (
        <div className="extracted-text-section">
          <h4>Extracted Text:</h4>
          <p className="extracted-text">{extractedText}</p>
        </div>
      )}

      <div className="response-section">
        <h4>Analysis:</h4>
        <div className="response-text">{response}</div>
      </div>

      {citations && citations.length > 0 && (
        <div className="citations-section">
          <h4>Sources & Citations:</h4>
          <ul className="citations-list">
            {citations.map((citation, index) => (
              <li key={index} className="citation-item">
                <a
                  href={citation.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="citation-link"
                >
                  {citation.title}
                </a>
                {citation.snippet && <p className="citation-snippet">{citation.snippet}</p>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ResultCard;
