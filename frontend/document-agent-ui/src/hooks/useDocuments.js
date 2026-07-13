/**
 * useDocuments Hook
 * Custom hook for document management
 */

import { useState, useEffect } from 'react';
import { documentStore } from '../stores';
import { documentAPI } from '../services/api/documents';
import { createLogger } from '../utils';

const logger = createLogger('useDocuments');

export const useDocuments = (page = 1, pageSize = 10) => {
  const [documents, setDocuments] = useState(documentStore.documents);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      setLoading(true);
      try {
        const response = await documentAPI.list(page, pageSize);
        console.log('📋 Documents API response:', response);

        // Handle both wrapped and direct array responses
        const docsList = Array.isArray(response)
          ? response
          : response.documents || response.data || [];
        console.log('📄 Parsed documents:', docsList);

        documentStore.setDocuments(docsList);
        documentStore.setTotal(response.total || docsList.length);
        setDocuments(docsList);
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

  const uploadDocument = async (file) => {
    try {
      logger.info('Uploading document', { filename: file.name });
      const response = await documentAPI.upload(file);
      logger.info('Document uploaded successfully');
      logger.debug('Upload response', { uploadResponse: response });
      // Refetch the list
      const listResponse = await documentAPI.list(page, pageSize);
      const docsList = Array.isArray(listResponse)
        ? listResponse
        : listResponse.documents || listResponse.data || [];
      documentStore.setDocuments(docsList);
      setDocuments(docsList);
      return response;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to upload document');
      setError(error);
      throw error;
    }
  };

  const deleteDocument = async (documentId) => {
    try {
      logger.info('Deleting document', { documentId });
      await documentAPI.delete(documentId);
      logger.info('Document deleted successfully');
      // Refetch the documents list
      const listResponse = await documentAPI.list(page, pageSize);
      const docsList = Array.isArray(listResponse)
        ? listResponse
        : listResponse.documents || listResponse.data || [];
      documentStore.setDocuments(docsList);
      setDocuments(docsList);
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
