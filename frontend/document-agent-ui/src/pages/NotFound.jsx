/**
 * Not Found Page
 * 404 page
 */

import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui';

export const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center space-y-6">
        <div className="text-6xl">😕</div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white">404 - Not Found</h1>
        <p className="text-gray-600 dark:text-gray-400 max-w-md">
          The page you are looking for might have been removed or is temporarily unavailable.
        </p>
        <Button onClick={() => navigate('/')}>Go to Dashboard</Button>
      </div>
    </div>
  );
};
