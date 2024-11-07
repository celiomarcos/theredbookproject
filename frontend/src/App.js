// src/App.js

import React, { Suspense, useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import LoadingSpinner from './components/LoadingSpinner';
import { AppRoutes } from './routes';

// Lazy load pages for better performance
const SearchPage = React.lazy(() => import('./pages/SearchPage'));
const HistoryPage = React.lazy(() => import('./pages/HistoryPage'));

// Navigation items configuration
const navigationItems = [
  { path: '/', label: 'Search', icon: '🔍' },
  { path: '/history', label: 'History', icon: '📜' }
];

const App = () => {
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(true);

  // Simulate initial app loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  // Navigation link component
  const NavLink = ({ path, label, icon }) => {
    const isActive = location.pathname === path;
    return (
      <Link
        to={path}
        className={`flex items-center px-4 py-2 rounded-md transition-colors duration-200 ${
          isActive
            ? 'bg-blue-100 text-blue-700'
            : 'text-gray-600 hover:bg-gray-100'
        }`}
      >
        <span className="mr-2">{icon}</span>
        <span className="font-medium">{label}</span>
      </Link>
    );
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo/Title */}
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">
                The Red Book Project
              </h1>
            </div>

            {/* Navigation */}
            <nav className="flex space-x-4">
              {navigationItems.map((item) => (
                <NavLink key={item.path} {...item} />
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <AppRoutes />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            The Red Book Project © {new Date().getFullYear()} - All rights by CelioSantiago
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;
