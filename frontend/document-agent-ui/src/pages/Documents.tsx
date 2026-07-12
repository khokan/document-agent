/**
 * Documents Page
 * Page for managing documents (upload, list, delete)
 */

import React, { useState } from 'react';
import { Card, CardBody, CardHeader, Button, Spinner, Badge } from '../components/ui';
import { useDocuments } from '../hooks';
import { formatFileSize, formatDate, formatStatus } from '../utils';

export const DocumentsPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const { documents, loading, error, uploadDocument, deleteDocument } = useDocuments();

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      await uploadDocument(selectedFile);
      setSelectedFile(null);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (documentId: string) => {
    if (confirm('Are you sure you want to delete this document?')) {
      await deleteDocument(documentId);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Documents</h1>
        <p className="text-gray-600 dark:text-gray-400">Manage your PDF documents</p>
      </div>

      <Card>
        <CardHeader>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Upload PDF</h2>
        </CardHeader>
        <CardBody className="space-y-4">
          <div className="border-2 border-dashed border-blue-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
              className="hidden"
              id="file-input"
            />
            <label htmlFor="file-input" className="cursor-pointer">
              <p className="text-4xl mb-2">📁</p>
              <p className="text-gray-700 dark:text-gray-300">
                {selectedFile ? selectedFile.name : 'Click to select or drag and drop a PDF file'}
              </p>
              {selectedFile && (
                <p className="text-sm text-gray-500 mt-2">{formatFileSize(selectedFile.size)}</p>
              )}
            </label>
          </div>
          <Button onClick={handleUpload} disabled={!selectedFile || uploading} isLoading={uploading}>
            Upload PDF
          </Button>
        </CardBody>
      </Card>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">{error.message}</p>
        </div>
      )}

      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recent Documents</h2>
        {loading ? (
          <Spinner message="Loading documents..." />
        ) : documents.length === 0 ? (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            <p className="text-lg">No documents found</p>
            <p className="text-sm">Upload your first PDF to get started</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {documents.map((doc) => {
              const document = doc as Record<string, unknown>;
              return (
                <Card key={String(document.id)}>
                  <CardBody>
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 dark:text-white">{String(document.filename)}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          📄 {String(document.pages)} pages • {formatFileSize(document.size as number)} •{' '}
                          {formatDate(String(document.upload_date))}
                        </p>
                      </div>
                      <div className="flex items-center gap-4">
                        <Badge label={formatStatus(document.status as string)} variant="success" />
                        <Button
                          variant="danger"
                          size="sm"
                          onClick={() => handleDelete(document.id as string)}
                        >
                          Delete
                        </Button>
                      </div>
                    </div>
                  </CardBody>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
