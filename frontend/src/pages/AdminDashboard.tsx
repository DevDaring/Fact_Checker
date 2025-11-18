import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import ResultCard from '../components/ResultCard';
import CommentBox from '../components/CommentBox';
import LoadingSpinner from '../components/LoadingSpinner';
import * as adminService from '../services/adminService';
import { User } from '../types/user';
import { FactCheck } from '../types/factCheck';
import { formatDate } from '../utils/formatters';

const AdminDashboard: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [userFactChecks, setUserFactChecks] = useState<FactCheck[]>([]);
  const [selectedFactCheck, setSelectedFactCheck] = useState<FactCheck | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const data = await adminService.getAllUsers();
      setUsers(data);
    } catch (err: any) {
      setError(err.detail || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleUserClick = async (user: User) => {
    setSelectedUser(user);
    setSelectedFactCheck(null);
    setError('');

    try {
      const checks = await adminService.getUserFactChecks(user.user_id);
      setUserFactChecks(checks);
    } catch (err: any) {
      setError(err.detail || 'Failed to load user fact-checks');
    }
  };

  const handleAddComment = async (commentText: string) => {
    if (!selectedFactCheck) return;

    try {
      await adminService.addComment(selectedFactCheck.fact_check_id, commentText);

      // Reload fact-check to get updated comments
      if (selectedUser) {
        const checks = await adminService.getUserFactChecks(selectedUser.user_id);
        setUserFactChecks(checks);

        const updated = checks.find(
          (c) => c.fact_check_id === selectedFactCheck.fact_check_id
        );
        if (updated) {
          setSelectedFactCheck(updated);
        }
      }
    } catch (err: any) {
      setError(err.detail || 'Failed to add comment');
    }
  };

  const handleBackToUsers = () => {
    setSelectedUser(null);
    setUserFactChecks([]);
    setSelectedFactCheck(null);
  };

  const handleBackToFactChecks = () => {
    setSelectedFactCheck(null);
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <Navbar />
        <LoadingSpinner message="Loading users..." />
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <Navbar />
      <div className="dashboard-container">
        {error && <div className="error-message">{error}</div>}

        {!selectedUser && (
          <>
            <div className="admin-header">
              <h2>All Users</h2>
              <p>{users.length} registered users</p>
            </div>

            <div className="users-list">
              {users.map((user) => (
                <div
                  key={user.user_id}
                  className="user-card"
                  onClick={() => handleUserClick(user)}
                >
                  <div className="user-info">
                    <h3>{user.email}</h3>
                    <span className={`role-badge ${user.role.toLowerCase()}`}>
                      {user.role}
                    </span>
                  </div>
                  <div className="user-meta">
                    <p>Joined: {formatDate(user.created_at)}</p>
                    <p>Last Login: {formatDate(user.last_login)}</p>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {selectedUser && !selectedFactCheck && (
          <>
            <button className="btn-back" onClick={handleBackToUsers}>
              ← Back to Users
            </button>

            <div className="admin-header">
              <h2>Fact-Checks by {selectedUser.email}</h2>
              <p>{userFactChecks.length} total fact-checks</p>
            </div>

            {userFactChecks.length === 0 ? (
              <div className="empty-state">
                <p>This user hasn't performed any fact-checks yet.</p>
              </div>
            ) : (
              <div className="fact-checks-list">
                {userFactChecks.map((factCheck) => (
                  <div
                    key={factCheck.fact_check_id}
                    className="fact-check-card"
                    onClick={() => setSelectedFactCheck(factCheck)}
                  >
                    <div className="fact-check-header">
                      <span className="upload-type-badge">{factCheck.upload_type}</span>
                      <span className="timestamp">{formatDate(factCheck.timestamp)}</span>
                    </div>
                    <p className="fact-check-preview">
                      {factCheck.gemini_response.substring(0, 200)}...
                    </p>
                    {factCheck.admin_comments && factCheck.admin_comments.length > 0 && (
                      <span className="comment-count">
                        {factCheck.admin_comments.length} comment(s)
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {selectedFactCheck && (
          <>
            <button className="btn-back" onClick={handleBackToFactChecks}>
              ← Back to Fact-Checks
            </button>

            <ResultCard
              extractedText={selectedFactCheck.extracted_text}
              response={selectedFactCheck.gemini_response}
              citations={selectedFactCheck.citations}
            />

            <CommentBox
              comments={selectedFactCheck.admin_comments || []}
              onAddComment={handleAddComment}
              isAdmin={true}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
