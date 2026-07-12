import React from 'react';
import { Layout } from './components/layout';
import { DashboardPage, DocumentsPage, SearchPage, NotFound } from './pages';

const App: React.FC = () => {
  const getCurrentPage = () => {
    const hash = window.location.hash.slice(1) || '/';

    switch (hash) {
      case '/':
        return <DashboardPage />;
      case '/documents':
        return <DocumentsPage />;
      case '/search':
        return <SearchPage />;
      default:
        return <NotFound />;
    }
  };

  return (
    <Layout>
      {getCurrentPage()}
    </Layout>
  );
};

export default App;
