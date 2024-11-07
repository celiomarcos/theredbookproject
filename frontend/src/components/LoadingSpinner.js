// src/components/LoadingSpinner.js

import React from 'react';

const LoadingSpinner = ({ size = 'default' }) => {
  const sizeClasses = {
    small: 'h-4 w-4 border-2',
    default: 'h-8 w-8 border-3',
    large: 'h-12 w-12 border-4'
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <div
        className={`animate-spin rounded-full border-b-transparent border-blue-600 ${
          sizeClasses[size] || sizeClasses.default
        }`}
      />
      <span className="mt-2 text-sm text-gray-500">Loading...</span>
    </div>
  );
};

export default LoadingSpinner;