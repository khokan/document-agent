/**
 * useDocuments Hook
 * Custom hook for document management
 */

import { useState, useEffect } from 'react';
import { documentStore } from '../stores';
import { documentAPI } from '../services/api/documents';
import { createLogger } from '../utils';

const logger = createLogger('useDocuments');

export const useDocuments = (page: number = 1, pageSize: number = 10) => {
  const [documents, setDocuments] = useState(documentStore.documents);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      setLoading(true);
      try {
        const response = await documentAPI.list(page, pageSize);
        documentStore.setDocuments(response.documents);
        documentStore.setTotal(response.total);
        setDocuments(response.documents);
      } catch (err) {
        const error = err instanceof Error ? err : new Error('Failed to fetch documents');
        setError(error);
        logger.error('Failed to fetch documents', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, [page, pageSize]);

  const uploadDocument = async (file: File) => {
    try {
      logger.info('Uploading document', { filename: file.name });
      const response = await documentAPI.upload(file);
      logger.info('Document uploaded successfully');
      logger.debug('Upload response', { uploadResponse: response });
      // Refetch the list
      const listResponse = await documentAPI.list(page, pageSize);
      documentStore.setDocuments(listResponse.documents);
      setDocuments(listResponse.documents);
      return response;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to upload document');
      setError(error);
      throw error;
    }
  };

  const deleteDocument = async (documentId: string) => {
    try {
      logger.info('Deleting document', { documentId });
      await documentAPI.delete(documentId);
      // Remove from local state
      setDocuments((prev) => prev.filter((doc) => (doc as Record<string, unknown>).id !== documentId));
      logger.info('Document deleted successfully');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to delete document');
      setError(error);
      throw error;
    }
  };

  return {
    documents,
    loading,
    error,
    uploadDocument,
    deleteDocument,
    total: documentStore.total,
  };
};
