import React, { useState } from 'react';
import { Comment } from '../types/factCheck';
import { formatDate } from '../utils/formatters';

interface CommentBoxProps {
  comments: Comment[];
  onAddComment?: (text: string) => void;
  isAdmin?: boolean;
}

const CommentBox: React.FC<CommentBoxProps> = ({ comments, onAddComment, isAdmin = false }) => {
  const [newComment, setNewComment] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!newComment.trim() || !onAddComment) return;

    setSubmitting(true);
    try {
      await onAddComment(newComment);
      setNewComment('');
    } catch (error) {
      console.error('Error adding comment:', error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="comment-box">
      <h4>Admin Comments</h4>

      {comments.length === 0 ? (
        <p className="no-comments">No comments yet</p>
      ) : (
        <div className="comments-list">
          {comments.map((comment) => (
            <div key={comment.comment_id} className="comment-item">
              <div className="comment-header">
                <span className="comment-author">{comment.admin_email}</span>
                <span className="comment-time">{formatDate(comment.timestamp)}</span>
              </div>
              <p className="comment-text">{comment.comment_text}</p>
            </div>
          ))}
        </div>
      )}

      {isAdmin && onAddComment && (
        <div className="add-comment-section">
          <textarea
            className="comment-input"
            placeholder="Add a comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            disabled={submitting}
          />
          <button
            className="btn-submit-comment"
            onClick={handleSubmit}
            disabled={!newComment.trim() || submitting}
          >
            {submitting ? 'Submitting...' : 'Add Comment'}
          </button>
        </div>
      )}
    </div>
  );
};

export default CommentBox;
