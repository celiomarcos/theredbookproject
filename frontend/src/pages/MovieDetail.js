// src/pages/MovieDetail.js
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { usePageTitle } from '../hooks/usePageTitle';
import LoadingSpinner from '../components/LoadingSpinner';

const MovieDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  usePageTitle(movie?.name || 'Movie Details');

  useEffect(() => {
    const fetchMovieDetails = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/movies/${id}`);
        if (!response.ok) throw new Error('Movie not found');
        const data = await response.json();
        setMovie(data.movie);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMovieDetails();
  }, [id]);

  if (loading) return <LoadingSpinner />;
  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">{error}</p>
        <button
          onClick={() => navigate(-1)}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Go Back
        </button>
      </div>
    );
  }

  if (!movie) return null;

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="px-6 py-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{movie.name}</h1>
          <div className="flex items-center text-gray-600">
            <span className="mr-4">Runtime: {movie.runtimeInMinutes} minutes</span>
            <span>Released: {new Date(movie.released).getFullYear()}</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h2 className="text-xl font-semibold mb-2">Box Office</h2>
            <div className="bg-gray-50 p-4 rounded">
              <p>Budget: ${movie.budgetInMillions}M</p>
              <p>Revenue: ${movie.boxOfficeRevenueInMillions}M</p>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-2">Awards</h2>
            <div className="bg-gray-50 p-4 rounded">
              <p>Academy Award Nominations: {movie.academyAwardNominations}</p>
              <p>Academy Award Wins: {movie.academyAwardWins}</p>
            </div>
          </div>
        </div>

        <div className="mt-8">
          <button
            onClick={() => navigate(-1)}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
          >
            Back to Search
          </button>
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;