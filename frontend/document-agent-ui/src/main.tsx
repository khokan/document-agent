import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

console.log('🚀 main.tsx loaded');
const rootElement = document.getElementById('root');
console.log('📍 Root element:', rootElement);

try {
  if (rootElement) {
    console.log('✅ Root element found, rendering App...');
    ReactDOM.createRoot(rootElement).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    console.log('✅ App rendered successfully');
  } else {
    console.error('❌ Root element not found!');
  }
} catch (error) {
  console.error('❌ Error rendering app:', error);
  if (rootElement) {
    rootElement.innerHTML = `<div style="padding: 20px; color: red;"><h1>Error Loading App</h1><pre>${error}</pre></div>`;
  }
}
