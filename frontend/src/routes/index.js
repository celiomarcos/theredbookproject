import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';

// Lazy load components for better performance
const SearchPage = React.lazy(() => import('../pages/SearchPage'));
const HistoryPage = React.lazy(() => import('../pages/HistoryPage'));
const MovieDetail = React.lazy(() => import('../pages/MovieDetail'));
const NotFound = React.lazy(() => import('../pages/NotFound'));

// Layout wrapper component
const PageLayout = ({ children }) => (
  <div className="bg-white shadow rounded-lg p-6">
    {children}
  </div>
);

// Routes configuration
export const AppRoutes = () => {
  return (
    <Suspense
      fallback={
        <div className="flex justify-center items-center h-64">
          <LoadingSpinner />
        </div>
      }
    >
      <Routes>
        <Route
          path="/"
          element={
            <PageLayout>
              <SearchPage />
            </PageLayout>
          }
        />
        <Route
          path="/history"
          element={
            <PageLayout>
              <HistoryPage />
            </PageLayout>
          }
        />
        <Route
          path="/movie/:id"
          element={
            <PageLayout>
              <MovieDetail />
            </PageLayout>
          }
        />
        <Route path="/404" element={<NotFound />} />
        <Route path="*" element={<Navigate to="/404" replace />} />
      </Routes>
    </Suspense>
  );
};