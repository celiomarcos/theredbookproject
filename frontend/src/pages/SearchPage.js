// src/pages/SearchPage.js
import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePageTitle } from '../hooks/usePageTitle';
import { useDebounce } from '../hooks/useDebounce';
import LoadingSpinner from '../components/LoadingSpinner';

const SearchPage = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  usePageTitle('Search Movies');

  // Debounce search term to avoid too many API calls
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  const handleSearch = useCallback(async () => {
    if (!userName.trim()) {
      setError('Please enter your name');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:5000/api/movies?name=${encodeURIComponent(debouncedSearchTerm)}&user=${encodeURIComponent(userName)}`
      );
      
      if (!response.ok) throw new Error('Failed to fetch movies');
      
      const data = await response.json();
      setResults(data.movies);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [debouncedSearchTerm, userName]);

  // Effect to trigger search when debounced term changes
  React.useEffect(() => {
    if (debouncedSearchTerm && userName) {
      handleSearch();
    }
  }, [debouncedSearchTerm, userName, handleSearch]);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Search Lord of the Rings Movies</h1>
        <div className="space-y-4">
          <div>
            <label htmlFor="userName" className="block text-sm font-medium text-gray-700">
              Your Name
            </label>
            <input
              type="text"
              id="userName"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Enter your name"
            />
          </div>

          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700">
              Movie Name
            </label>
            <input
              type="text"
              id="search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Search for a movie..."
            />
          </div>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
            {error}
          </div>
        )}
      </div>

      {loading ? (
        <div className="flex justify-center my-8">
          <LoadingSpinner />
        </div>
      ) : (
        <div className="space-y-4">
          {results.map((movie) => (
            <div
              key={movie._id}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => navigate(`/movie/${movie._id}`)}
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-2">{movie.name}</h2>
              <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                <div>
                  <p>Runtime: {movie.runtimeInMinutes} minutes</p>
                  <p>Budget: ${movie.budgetInMillions}M</p>
                </div>
                <div>
                  <p>Box Office: ${movie.boxOfficeRevenueInMillions}M</p>
                  <p>Awards: {movie.academyAwardWins} Academy Awards</p>
                </div>
              </div>
            </div>
          ))}
          
          {!loading && results.length === 0 && searchTerm && (
            <p className="text-center text-gray-600">No movies found matching your search.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchPage;