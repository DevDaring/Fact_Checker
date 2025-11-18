import { useState } from 'react';
import * as uploadService from '../services/uploadService';
import { UploadResponse } from '../types/factCheck';

interface UseFileUploadReturn {
  uploadFile: (file: File, type: 'video' | 'audio' | 'image') => Promise<UploadResponse>;
  uploading: boolean;
  progress: number;
  error: string | null;
}

export const useFileUpload = (): UseFileUploadReturn => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const uploadFile = async (
    file: File,
    type: 'video' | 'audio' | 'image'
  ): Promise<UploadResponse> => {
    setUploading(true);
    setProgress(0);
    setError(null);

    try {
      let response: UploadResponse;

      // Simulate progress (since we can't track actual upload progress with current setup)
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      if (type === 'video') {
        response = await uploadService.uploadVideo(file);
      } else if (type === 'audio') {
        response = await uploadService.uploadAudio(file);
      } else {
        response = await uploadService.uploadImage(file);
      }

      clearInterval(progressInterval);
      setProgress(100);

      return response;
    } catch (err: any) {
      setError(err.detail || 'Upload failed');
      throw err;
    } finally {
      setUploading(false);
    }
  };

  return {
    uploadFile,
    uploading,
    progress,
    error,
  };
};
