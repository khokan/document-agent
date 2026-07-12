/**
 * Layout Component
 * Main layout wrapper for the application
 */

import React from 'react';
import type { ReactNode } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface LayoutProps {
  children: ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 ml-0 lg:ml-64 overflow-auto">
          <div className="p-6">{children}</div>
        </main>
      </div>
    </div>
  );
};
