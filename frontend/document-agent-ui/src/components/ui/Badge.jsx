/**
 * Badge Component
 * Reusable badge/tag component
 */

export const Badge = ({ label, variant = 'default', className = '' }) => {
  const variantStyles = {
    success: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    warning: 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    default: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
  };

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${variantStyles[variant]} ${className}`}>
      {label}
    </span>
  );
};
