import api from './api';
import { User } from '../types/user';
import { FactCheck, Comment } from '../types/factCheck';
import { ApiResponse } from '../types/api';

export const getAllUsers = async (): Promise<User[]> => {
  const response = await api.get<ApiResponse<User[]>>('/api/admin/users');
  return response.data.data || [];
};

export const getAllFactChecks = async (): Promise<FactCheck[]> => {
  const response = await api.get<ApiResponse<FactCheck[]>>('/api/admin/fact-checks');
  return response.data.data || [];
};

export const getUserFactChecks = async (userId: number): Promise<FactCheck[]> => {
  const response = await api.get<ApiResponse<FactCheck[]>>(
    `/api/admin/user-checks/${userId}`
  );
  return response.data.data || [];
};

export const addComment = async (
  factCheckId: number,
  commentText: string
): Promise<Comment> => {
  const response = await api.post<Comment>('/api/admin/comment', {
    fact_check_id: factCheckId,
    comment_text: commentText,
  });
  return response.data;
};

export const getComments = async (factCheckId: number): Promise<Comment[]> => {
  const response = await api.get<ApiResponse<Comment[]>>(
    `/api/admin/comments/${factCheckId}`
  );
  return response.data.data || [];
};
