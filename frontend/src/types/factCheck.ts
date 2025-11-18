export interface Citation {
  title: string;
  url: string;
  snippet?: string;
}

export interface FactCheck {
  fact_check_id: number;
  user_id: number;
  upload_type: 'video' | 'audio' | 'image';
  file_path: string;
  extracted_text?: string;
  gemini_response: string;
  citations: Citation[];
  timestamp: string;
  admin_comments?: Comment[];
}

export interface FactCheckResult {
  fact_check_id: number;
  extracted_text?: string;
  gemini_response: string;
  citations: Citation[];
  timestamp: string;
}

export interface Comment {
  comment_id: number;
  fact_check_id: number;
  admin_id: number;
  admin_email: string;
  comment_text: string;
  timestamp: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  data: {
    file_id: string;
    file_path: string;
    upload_type: string;
  };
}
