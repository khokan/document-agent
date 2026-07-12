/**
 * Sidebar Component
 * Application sidebar with navigation links
 */

import React, { useState, useEffect } from 'react';
import { uiStore } from '../../stores';

interface NavLink {
  label: string;
  href: string;
  icon: string;
}

const navLinks: NavLink[] = [
  { label: 'Dashboard', href: '#/', icon: '📊' },
  { label: 'Documents', href: '#/documents', icon: '📁' },
  { label: 'Search', href: '#/search', icon: '🔍' },
  { label: 'Settings', href: '#/settings', icon: '⚙️' },
];

export const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(uiStore.sidebarOpen);

  useEffect(() => {
    const unsubscribe = uiStore.subscribe(() => {
      setIsOpen(uiStore.sidebarOpen);
    });
    return unsubscribe;
  }, []);

  return (
    <aside
      className={`fixed left-0 top-16 h-[calc(100vh-64px)] w-64 bg-gray-100 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-transform duration-300 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      } z-40`}
    >
      <nav className="p-4 space-y-2">
        {navLinks.map((link) => (
          <a
            key={link.href}
            href={link.href}
            className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          >
            <span className="text-xl">{link.icon}</span>
            <span className="font-medium text-gray-900 dark:text-white">{link.label}</span>
          </a>
        ))}
      </nav>
    </aside>
  );
};
