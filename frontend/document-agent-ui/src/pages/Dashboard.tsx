/**
 * Dashboard Page
 * Main dashboard showing system statistics and recent documents
 */

import React, { useState, useEffect } from 'react';
import { Card, CardBody, CardHeader, Spinner } from '../components/ui';
import { formatFileSize, formatNumber } from '../utils';
import { documentAPI } from '../services/api/documents';
import type { DocumentStats } from '../types';

export const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DocumentStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await documentAPI.getStats();
        setStats(response);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch statistics'));
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <Spinner size="lg" message="Loading dashboard..." />;
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-200">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">Welcome to PDF Knowledge Assistant</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Total Documents</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                  {formatNumber((stats?.total_documents as number) || 0)}
                </p>
              </div>
              <span className="text-4xl">📄</span>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Total Pages</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                  {formatNumber((stats?.total_pages as number) || 0)}
                </p>
              </div>
              <span className="text-4xl">📑</span>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Total Size</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                  {formatFileSize(((stats?.total_size_mb as number) || 0) * 1024 * 1024)}
                </p>
              </div>
              <span className="text-4xl">💾</span>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Processing</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                  {formatNumber((stats?.processing_documents as number) || 0)}
                </p>
              </div>
              <span className="text-4xl">⚙️</span>
            </div>
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Quick Actions</h2>
        </CardHeader>
        <CardBody className="space-y-2">
          <a href="#/documents" className="block p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
            📤 Upload Documents
          </a>
          <a href="#/search" className="block p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
            🔍 Search Knowledge Base
          </a>
          <a href="#/settings" className="block p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
            ⚙️ System Settings
          </a>
        </CardBody>
      </Card>
    </div>
  );
};
