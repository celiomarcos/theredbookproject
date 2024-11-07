// src/index.js

import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App';
import ErrorBoundary from './components/ErrorBoundary';
import reportWebVitals from './reportWebVitals';

// Initialize any global error handlers
window.addEventListener('unhandledrejection', (event) => {
  // Log error to your error tracking service in production
  console.error('Unhandled promise rejection:', event.reason);
});

// Optional: Add performance monitoring
const reportPerformance = (metric) => {
  // You can send metrics to your analytics service here
  if (process.env.NODE_ENV === 'development') {
    console.log(metric);
  }
};

// Optional: Add global variables to window for development
if (process.env.NODE_ENV === 'development') {
  window.DEBUG = {
    logError: (error) => console.error('Debug Error:', error),
    logInfo: (info) => console.info('Debug Info:', info)
  };
}

// Get the root element and handle potential missing root
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Failed to find the root element');
}

// Create root with error handling
try {
  const root = createRoot(rootElement);

  // Render app with all providers
  root.render(
    <React.StrictMode>
      <ErrorBoundary>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ErrorBoundary>
    </React.StrictMode>
  );

  // Report web vitals
  reportWebVitals(reportPerformance);
} catch (error) {
  console.error('Error rendering application:', error);
  
  // Show a basic error message if the app fails to render
  rootElement.innerHTML = `
    <div style="
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      text-align: center;
      font-family: sans-serif;
    ">
      <h1 style="color: #e53e3e;">Unable to load application</h1>
      <p>Please try refreshing the page. If the problem persists, contact support.</p>
    </div>
  `;
}

// Enable Hot Module Replacement (HMR) in development
if (process.env.NODE_ENV === 'development' && module.hot) {
  module.hot.accept('./App', () => {
    // Reload the application when changes are detected
    const NextApp = require('./App').default;
    createRoot(rootElement).render(
      <React.StrictMode>
        <ErrorBoundary>
          <BrowserRouter>
            <NextApp />
          </BrowserRouter>
        </ErrorBoundary>
      </React.StrictMode>
    );
  });
}

// Clean up on unmount (useful for preventing memory leaks)
window.addEventListener('unload', () => {
  // Perform any necessary cleanup
  reportWebVitals(reportPerformance);
});