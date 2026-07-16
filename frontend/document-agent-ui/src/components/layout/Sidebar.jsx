/**
 * Sidebar Component
 * Application sidebar with navigation links
 */

import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { uiStore } from '../../stores';

const navLinks = [
  { label: 'Dashboard', to: '/', icon: '📊' },
  { label: 'Documents', to: '/documents', icon: '📁' },
  { label: 'Search', to: '/search', icon: '🔍' },
  { label: 'Ask (RAG)', to: '/ask', icon: '🤖' },
  { label: 'Chat', to: '/chat', icon: '💬' },
  { label: 'Summarize', to: '/summarize', icon: '📝' },
];

export const Sidebar = () => {
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
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                  : 'hover:bg-gray-200 dark:hover:bg-gray-700'
              }`
            }
          >
            <span className="text-xl">{link.icon}</span>
            <span className="font-medium text-gray-900 dark:text-white">{link.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};
