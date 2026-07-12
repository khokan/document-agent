/**
 * Spinner Component
 * Loading spinner component
 */

export const Spinner = ({ size = 'md', message }) => {
  const sizeStyles = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className={`${sizeStyles[size]} border-4 border-gray-300 border-t-blue-600 rounded-full animate-spin`} />
      {message && <p className="text-gray-600 dark:text-gray-400">{message}</p>}
    </div>
  );
};
