/**
 * Validators Utility
 * File and form validation utilities
 */

// Allowed MIME types
const ALLOWED_MIME_TYPES = ['application/pdf'];
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
const MAX_FILE_SIZE_MB = 50;

export const validatePdfFile = (file) => {
  // Check MIME type
  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: `Invalid file type. Only PDF files are allowed. Received: ${file.type}`,
    };
  }

  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      error: `File is too large. Maximum size is ${MAX_FILE_SIZE_MB}MB. Received: ${(file.size / 1024 / 1024).toFixed(2)}MB`,
    };
  }

  // Check file name
  if (!file.name || file.name.trim() === '') {
    return {
      valid: false,
      error: 'File name is empty',
    };
  }

  return { valid: true };
};

export const validateFiles = (files) => {
  const errors = new Map();

  files.forEach((file) => {
    const validation = validatePdfFile(file);
    if (!validation.valid && validation.error) {
      errors.set(file.name, validation.error);
    }
  });

  return {
    valid: errors.size === 0,
    errors,
  };
};

export const validateSearchQuery = (query) => {
  const trimmed = query.trim();

  if (!trimmed) {
    return {
      valid: false,
      error: 'Search query cannot be empty',
    };
  }

  if (trimmed.length < 2) {
    return {
      valid: false,
      error: 'Search query must be at least 2 characters',
    };
  }

  if (trimmed.length > 500) {
    return {
      valid: false,
      error: 'Search query must be less than 500 characters',
    };
  }

  return { valid: true };
};

export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateUrl = (url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};
