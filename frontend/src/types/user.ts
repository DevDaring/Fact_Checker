export interface User {
  user_id: number;
  email: string;
  role: 'User' | 'Admin';
  created_at: string;
  last_login: string;
}

export interface LoginRequest {
  email: string;
  password: string;
  role: 'User' | 'Admin';
}

export interface RegisterRequest {
  email: string;
  password: string;
  role: 'User' | 'Admin';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
