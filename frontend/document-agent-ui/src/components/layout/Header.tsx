/**
 * Header Component
 * Application header with navigation
 */

import React, { useState, useEffect } from 'react';
import { uiStore } from '../../stores';
import { Button } from '../ui';

export const Header: React.FC = () => {
  const [darkMode, setDarkMode] = useState(uiStore.darkMode);

  useEffect(() => {
    const unsubscribe = uiStore.subscribe(() => {
      setDarkMode(uiStore.darkMode);
    });
    return unsubscribe;
  }, []);

  const toggleDarkMode = () => {
    uiStore.toggleDarkMode();
  };

  const toggleSidebar = () => {
    uiStore.toggleSidebar();
  };

  return (
    <header className="bg-white dark:bg-gray-900 shadow-md border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-4">
          <button onClick={toggleSidebar} className="text-2xl hover:text-blue-600 transition-colors">
            ☰
          </button>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">📄 PDF Knowledge Assistant</h1>
        </div>

        <div className="flex items-center gap-4">
          <Button variant="outline" size="sm" onClick={toggleDarkMode}>
            {darkMode ? '☀️' : '🌙'}
          </Button>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
              U
            </div>
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">User</span>
          </div>
        </div>
      </div>
    </header>
  );
};
