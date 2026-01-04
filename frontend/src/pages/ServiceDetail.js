import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import api from '../utils/api';
import { useAuth } from '../contexts/AuthContext';

const ServiceDetail = () => {
  const { id } = useParams();
  const { user, isAuthenticated } = useAuth();

  const { data: service, isLoading } = useQuery(
    ['service', id],
    async () => {
      const response = await api.get(`/services/${id}/`);
      return response.data;
    }
  );

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!service) {
    return <div className="text-center py-12">Service introuvable</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {service.image_principale && (
          <img
            src={service.image_principale}
            alt={service.titre}
            className="w-full h-96 object-cover"
          />
        )}
        
        <div className="p-8">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-3xl font-bold mb-2">{service.titre}</h1>
              <p className="text-gray-600">{service.categorie?.nom}</p>
            </div>
            <div className="text-right">
              <p className="text-3xl font-bold text-primary-600">
                {service.prix_actuel} MRU
              </p>
              {service.est_en_promotion && (
                <p className="text-sm text-gray-500 line-through">
                  {service.prix} MRU
                </p>
              )}
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Description</h2>
            <p className="text-gray-700">{service.description}</p>
          </div>

          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Prestataire</h2>
            <div className="flex items-center space-x-4">
              {service.prestataire?.profil_photo && (
                <img
                  src={service.prestataire.profil_photo}
                  alt={service.prestataire.username}
                  className="w-16 h-16 rounded-full"
                />
              )}
              <div>
                <p className="font-semibold">{service.prestataire?.username}</p>
                {service.prestataire?.note_moyenne > 0 && (
                  <p className="text-sm text-gray-600">
                    ⭐ {service.prestataire.note_moyenne} ({service.prestataire.nombre_evaluations} avis)
                  </p>
                )}
              </div>
            </div>
          </div>

          {service.ville && (
            <div className="mb-6">
              <p className="text-gray-600">
                📍 {service.ville} {service.quartier && `- ${service.quartier}`}
              </p>
            </div>
          )}

          {isAuthenticated && user?.role === 'client' && (
            <div className="mt-8">
              <Link
                to={`/services/${id}/commander`}
                className="bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
              >
                Commander ce service
              </Link>
            </div>
          )}

          {isAuthenticated && user?.id === service.prestataire?.id && (
            <div className="mt-8">
              <Link
                to={`/services/${id}/edit`}
                className="bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-700 transition"
              >
                Modifier le service
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ServiceDetail;

