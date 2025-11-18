import api from './api';
import { AuthResponse, LoginRequest, RegisterRequest } from '../types/user';

export const login = async (
  email: string,
  password: string,
  role: 'User' | 'Admin'
): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/api/auth/login', {
    email,
    password,
    role,
  });
  return response.data;
};

export const register = async (data: RegisterRequest): Promise<any> => {
  const response = await api.post('/api/auth/register', data);
  return response.data;
};

export const logout = async (): Promise<void> => {
  await api.post('/api/auth/logout');
};
