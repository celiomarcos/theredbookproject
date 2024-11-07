// src/hooks/usePageTitle.js

import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const DEFAULT_TITLE = 'The Red Book Project';

// Title configuration for different routes
const ROUTE_TITLES = {
  '/': 'Search Movies - The Red Book Project',
  '/history': 'Search History - The Red Book Project',
  '/404': 'Page Not Found - The Red Book Project',
};

/**
 * Custom hook for managing page titles
 * @param {string} customTitle - Optional custom title to override default route title
 * @param {boolean} includeBaseName - Whether to include the base name in the title
 * @returns {void}
 */
export const usePageTitle = (customTitle = '', includeBaseName = true) => {
  const location = useLocation();

  useEffect(() => {
    // Function to build the page title
    const buildPageTitle = () => {
      // If a custom title is provided, use it
      if (customTitle) {
        return includeBaseName ? `${customTitle} - ${DEFAULT_TITLE}` : customTitle;
      }

      // Get the route-based title or use a default format
      const routeTitle = ROUTE_TITLES[location.pathname];
      if (routeTitle) {
        return routeTitle;
      }

      // For dynamic routes or unknown paths, create a formatted title
      const pathSegments = location.pathname.split('/').filter(Boolean);
      if (pathSegments.length > 0) {
        const formattedSegment = pathSegments[pathSegments.length - 1]
          .split('-')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');
        return includeBaseName 
          ? `${formattedSegment} - ${DEFAULT_TITLE}`
          : formattedSegment;
      }

      // Fallback to default title
      return DEFAULT_TITLE;
    };

    // Set the document title
    const newTitle = buildPageTitle();
    if (document.title !== newTitle) {
      document.title = newTitle;
    }

    // Optional: Log title changes in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`Page title updated to: ${newTitle}`);
    }

    // Clean up function
    return () => {
      // Reset to default title when component unmounts
      // Comment out if you don't want this behavior
      // document.title = DEFAULT_TITLE;
    };
  }, [location, customTitle, includeBaseName]);
};

// Example usage with TypeScript types (if using TypeScript)
/*
interface UsePageTitleOptions {
  customTitle?: string;
  includeBaseName?: boolean;
}

export const usePageTitle = ({ 
  customTitle = '', 
  includeBaseName = true 
}: UsePageTitleOptions = {}) => {
  // ... same implementation
};
*/

// Export additional utilities if needed
export const setCustomPageTitle = (title: string) => {
  document.title = title.includes(DEFAULT_TITLE) 
    ? title 
    : `${title} - ${DEFAULT_TITLE}`;
};

// Usage examples:
/*
// Basic usage
usePageTitle();

// With custom title
usePageTitle('Custom Page Title');

// Without base name
usePageTitle('Standalone Title', false);

// With dynamic content
usePageTitle(`Movie: ${movieName}`);
*/

export default usePageTitle;