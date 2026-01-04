import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import api from '../utils/api';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

const Messages = () => {
  const { user } = useAuth();
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messageText, setMessageText] = useState('');
  const queryClient = useQueryClient();

  // 1. Fetch des conversations (Sécurisé pour Django Rest Framework)
  const { data: conversations = [], isLoading: isLoadingConv } = useQuery('conversations', async () => {
    const response = await api.get('/messaging/conversations/');
    // On vérifie si c'est une liste paginée (response.data.results) ou une liste simple (response.data)
    const data = response.data.results || response.data;
    return Array.isArray(data) ? data : [];
  });

  // 2. Fetch des messages d'une conversation
  const { data: messages = [], isLoading: isLoadingMessages } = useQuery(
    ['messages', selectedConversation],
    async () => {
      if (!selectedConversation) return [];
      const response = await api.get('/messaging/messages/', {
        params: { conversation: selectedConversation },
      });
      const data = response.data.results || response.data;
      return Array.isArray(data) ? data : [];
    },
    { enabled: !!selectedConversation }
  );

  // 3. Mutation pour envoyer un message
  const sendMessageMutation = useMutation(
    async (newMsg) => {
      const response = await api.post('/messaging/messages/', newMsg);
      return response.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['messages', selectedConversation]);
        queryClient.invalidateQueries('conversations'); // Pour mettre à jour le "dernier message"
        setMessageText('');
        toast.success('Message envoyé');
      },
      onError: () => {
        toast.error("Erreur lors de l'envoi");
      }
    }
  );

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!messageText.trim() || !selectedConversation) return;

    sendMessageMutation.mutate({
      conversation: selectedConversation,
      contenu: messageText,
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Messages</h1>

      <div className="bg-white rounded-lg shadow-lg flex" style={{ height: '600px' }}>
        
        {/* Liste des conversations (Gauche) */}
        <div className="w-1/3 border-r overflow-y-auto">
          {isLoadingConv ? (
            <p className="p-4 text-center">Chargement...</p>
          ) : conversations.length > 0 ? (
            conversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => setSelectedConversation(conv.id)}
                className={`p-4 border-b cursor-pointer hover:bg-gray-50 ${
                  selectedConversation === conv.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="font-semibold text-gray-800">
                    {conv.participants
                      ?.filter((p) => p.id !== user?.id)
                      .map((p) => p.username || p.email)
                      .join(', ')}
                  </div>
                  {conv.nombre_messages_non_lus > 0 && (
                    <span className="bg-red-500 text-white rounded-full px-2 py-1 text-xs font-bold">
                      {conv.nombre_messages_non_lus}
                    </span>
                  )}
                </div>
                {conv.dernier_message && (
                  <p className="text-sm text-gray-500 truncate mt-1 italic">
                    {conv.dernier_message.contenu}
                  </p>
                )}
              </div>
            ))
          ) : (
            <p className="p-4 text-center text-gray-500">Aucune discussion</p>
          )}
        </div>

        {/* Zone de chat (Droite) */}
        <div className="flex-1 flex flex-col bg-gray-50">
          {selectedConversation ? (
            <>
              {/* Liste des messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {isLoadingMessages ? (
                   <p className="text-center">Chargement des messages...</p>
                ) : (
                  messages.map((message) => {
                    const isMe = message.expediteur?.id === user?.id;
                    return (
                      <div key={message.id} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl shadow-sm ${
                            isMe ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white text-gray-800 rounded-bl-none border'
                          }`}
                        >
                          {!isMe && <p className="text-xs font-bold mb-1 text-blue-500">{message.expediteur?.username}</p>}
                          <p className="text-sm">{message.contenu}</p>
                          <p className={`text-[10px] mt-1 ${isMe ? 'text-blue-100' : 'text-gray-400'}`}>
                            {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>

              {/* Formulaire d'envoi */}
              <form onSubmit={handleSendMessage} className="p-4 bg-white border-t">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    placeholder="Votre message pour Souq-Khidma..."
                    className="flex-1 px-4 py-2 border rounded-full focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                  <button
                    type="submit"
                    disabled={sendMessageMutation.isLoading}
                    className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition-colors disabled:bg-gray-400"
                  >
                    {sendMessageMutation.isLoading ? '...' : 'Envoyer'}
                  </button>
                </div>
              </form>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-gray-400">
              <span className="text-5xl mb-4">💬</span>
              <p>Sélectionnez une discussion pour commencer</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Messages;