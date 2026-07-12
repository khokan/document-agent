import { Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout';
import { DashboardPage, DocumentsPage, SearchPage, NotFound } from './pages';

const App = () => {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/documents" element={<DocumentsPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
};

export default App;
