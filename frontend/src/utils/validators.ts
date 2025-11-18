export const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const validatePassword = (password: string): { valid: boolean; message?: string } => {
  if (password.length < 6) {
    return { valid: false, message: 'Password must be at least 6 characters' };
  }
  return { valid: true };
};

export const validateFile = (
  file: File,
  type: 'video' | 'audio' | 'image',
  maxSizeMB: number = 100
): { valid: boolean; message?: string } => {
  const maxSize = maxSizeMB * 1024 * 1024;

  if (file.size > maxSize) {
    return { valid: false, message: `File size must be less than ${maxSizeMB}MB` };
  }

  const videoExtensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'];
  const audioExtensions = ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'];
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'];

  const fileName = file.name.toLowerCase();
  let validExtensions: string[] = [];

  if (type === 'video') {
    validExtensions = videoExtensions;
  } else if (type === 'audio') {
    validExtensions = audioExtensions;
  } else if (type === 'image') {
    validExtensions = imageExtensions;
  }

  const isValidExtension = validExtensions.some((ext) => fileName.endsWith(ext));

  if (!isValidExtension) {
    return { valid: false, message: `Invalid file type for ${type}` };
  }

  return { valid: true };
};
