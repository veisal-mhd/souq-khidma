import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import api from '../utils/api';

const Services = () => {
  const [filters, setFilters] = useState({
    categorie: '',
    prix_min: '',
    prix_max: '',
    ville: '',
    search: '',
  });

  const { data: services, isLoading } = useQuery(
    ['services', filters],
    async () => {
      const params = new URLSearchParams();
      if (filters.categorie) params.append('categorie', filters.categorie);
      if (filters.prix_min) params.append('prix_min', filters.prix_min);
      if (filters.prix_max) params.append('prix_max', filters.prix_max);
      if (filters.ville) params.append('ville', filters.ville);
      if (filters.search) params.append('search', filters.search);
      
      const response = await api.get(`/services/?${params.toString()}`);
      return response.data.results || response.data;
    }
  );

  const { data: categories } = useQuery('categories', async () => {
    const response = await api.get('/services/categories/');
    return response.data;
  });

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Services disponibles</h1>
      
      {/* Filtres */}
      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Recherche
            </label>
            <input
              type="text"
              name="search"
              placeholder="Rechercher..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={filters.search}
              onChange={handleFilterChange}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Catégorie
            </label>
            <select
              name="categorie"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={filters.categorie}
              onChange={handleFilterChange}
            >
              <option value="">Toutes</option>
              {categories?.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.nom}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Prix min (MRU)
            </label>
            <input
              type="number"
              name="prix_min"
              placeholder="Min"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={filters.prix_min}
              onChange={handleFilterChange}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Prix max (MRU)
            </label>
            <input
              type="number"
              name="prix_max"
              placeholder="Max"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={filters.prix_max}
              onChange={handleFilterChange}
            />
          </div>
        </div>
      </div>

      {/* Liste des services */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services?.map((service) => (
            <Link
              key={service.id}
              to={`/services/${service.id}`}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition"
            >
              {service.image_principale && (
                <img
                  src={service.image_principale}
                  alt={service.titre}
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">{service.titre}</h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {service.description}
                </p>
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-primary-600">
                    {service.prix_actuel} MRU
                  </span>
                  {service.est_en_promotion && (
                    <span className="bg-red-500 text-white px-2 py-1 rounded text-xs">
                      Promotion
                    </span>
                  )}
                </div>
                <div className="mt-4 text-sm text-gray-500">
                  <p>Par {service.prestataire?.username}</p>
                  {service.ville && <p>{service.ville}</p>}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
      
      {services?.length === 0 && !isLoading && (
        <div className="text-center py-12 text-gray-500">
          Aucun service trouvé
        </div>
      )}
    </div>
  );
};

export default Services;

