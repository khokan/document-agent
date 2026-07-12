/**
 * Document Type Definitions
 * Defines all document-related types
 */

export interface Document {
  id: string;
  filename: string;
  upload_date: string;
  size: number;
  pages: number;
  status: 'processing' | 'completed' | 'failed';
  error_message?: string;
  metadata?: {
    title?: string;
    author?: string;
    created?: string;
    [key: string]: unknown;
  };
}

export interface DocumentListResponse {
  documents: Document[];
  total: number;
  page: number;
  page_size: number;
}

export interface DocumentUploadRequest {
  file: File;
  metadata?: Record<string, string>;
}

export interface DocumentUploadResponse {
  id: string;
  filename: string;
  upload_date: string;
  status: string;
}

export interface DocumentDeleteResponse {
  success: boolean;
  message: string;
}

export interface DocumentStats {
  total_documents: number;
  total_pages: number;
  total_size_mb: number;
  processing_documents: number;
  failed_documents: number;
}
