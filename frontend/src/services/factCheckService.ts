import api from './api';
import { FactCheckResult, FactCheck } from '../types/factCheck';
import { ApiResponse } from '../types/api';

export const processFactCheck = async (
  filePath: string,
  uploadType: string
): Promise<FactCheckResult> => {
  const response = await api.post<FactCheckResult>('/api/fact-check/process', {
    file_path: filePath,
    upload_type: uploadType,
  });
  return response.data;
};

export const getFactCheckResult = async (factCheckId: number): Promise<FactCheck> => {
  const response = await api.get<ApiResponse<FactCheck>>(
    `/api/fact-check/result/${factCheckId}`
  );
  return response.data.data!;
};

export const getUserHistory = async (): Promise<FactCheck[]> => {
  const response = await api.get<ApiResponse<FactCheck[]>>('/api/history/user');
  return response.data.data || [];
};

export const getFactCheckDetails = async (factCheckId: number): Promise<FactCheck> => {
  const response = await api.get<ApiResponse<FactCheck>>(
    `/api/history/details/${factCheckId}`
  );
  return response.data.data!;
};
