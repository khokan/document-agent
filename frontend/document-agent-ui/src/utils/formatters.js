/**
 * Formatters Utility
 * Data formatting utilities
 */

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B';

  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
};

export const formatDate = (date) => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatDateTime = (date) => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatNumber = (num) => {
  return num.toLocaleString('en-US');
};

export const formatPercentage = (value, decimals = 0) => {
  return value.toFixed(decimals) + '%';
};

export const formatDuration = (ms) => {
  if (ms < 1000) {
    return ms.toFixed(0) + 'ms';
  }
  return (ms / 1000).toFixed(2) + 's';
};

export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + '...';
};

export const capitalizeFirstLetter = (text) => {
  if (!text) return '';
  return text.charAt(0).toUpperCase() + text.slice(1);
};

export const formatStatus = (status) => {
  return capitalizeFirstLetter(status.replace(/_/g, ' '));
};
