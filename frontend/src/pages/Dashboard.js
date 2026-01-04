import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useQuery } from 'react-query';
import api from '../utils/api';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();

  const { data: transactions } = useQuery(
    ['transactions', user?.id],
    async () => {
      if (user?.is_prestataire) {
        const response = await api.get('/transactions/mes_ventes/');
        return response.data;
      } else {
        const response = await api.get('/transactions/mes_commandes/');
        return response.data;
      }
    },
    { enabled: !!user }
  );

  const { data: services } = useQuery(
    ['mes_services', user?.id],
    async () => {
      const response = await api.get('/services/mes_services/');
      return response.data;
    },
    { enabled: user?.is_prestataire }
  );

  if (!user) return null;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">
        Tableau de bord - {user.is_prestataire ? 'Prestataire' : 'Client'}
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">Profil</h3>
          <p className="text-gray-600">{user.username}</p>
          <p className="text-sm text-gray-500">{user.email}</p>
          {user.is_prestataire && (
            <div className="mt-4">
              <p className="text-sm">
                Note moyenne: ⭐ {user.note_moyenne || 'N/A'} ({user.nombre_evaluations} avis)
              </p>
            </div>
          )}
        </div>

        {user.is_prestataire && (
          <>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-2">Mes services</h3>
              <p className="text-3xl font-bold text-primary-600">
                {services?.length || 0}
              </p>
              <Link to="/services/new" className="text-primary-600 text-sm mt-2 block">
                Ajouter un service
              </Link>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-2">Ventes</h3>
              <p className="text-3xl font-bold text-green-600">
                {transactions?.length || 0}
              </p>
            </div>
          </>
        )}

        {user.is_client && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">Mes commandes</h3>
            <p className="text-3xl font-bold text-primary-600">
              {transactions?.length || 0}
            </p>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">
          {user.is_prestataire ? 'Mes ventes récentes' : 'Mes commandes récentes'}
        </h2>
        {transactions?.length > 0 ? (
          <div className="space-y-4">
            {transactions.slice(0, 5).map((transaction) => (
              <div key={transaction.id} className="border-b pb-4">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-semibold">
                      {transaction.service?.titre || 'Service'}
                    </p>
                    <p className="text-sm text-gray-600">
                      {user.is_prestataire
                        ? `Client: ${transaction.client?.username}`
                        : `Prestataire: ${transaction.prestataire?.username}`}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(transaction.date_creation).toLocaleDateString('fr-FR')}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-lg">
                      {transaction.montant_total} MRU
                    </p>
                    <span
                      className={`px-2 py-1 rounded text-xs ${
                        transaction.statut === 'confirme'
                          ? 'bg-green-100 text-green-800'
                          : transaction.statut === 'en_escrow'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {transaction.statut}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">Aucune transaction pour le moment</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

