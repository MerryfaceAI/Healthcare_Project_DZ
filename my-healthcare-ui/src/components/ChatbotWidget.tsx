import React, { useState } from 'react';
import { FaComments, FaTimes } from 'react-icons/fa';

const ChatbotWidget: React.FC = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open && (
        <div
          role="dialog"
          aria-labelledby="chatbot-header"
          className="bg-white rounded-lg shadow-xl w-80 h-96 flex flex-col"
        >
          <div
            id="chatbot-header"
            className="flex items-center justify-between p-2 bg-blue-600 text-white rounded-t-lg"
          >
            <span className="text-sm font-medium">Help Bot</span>
            <button
              onClick={() => setOpen(false)}
              aria-label="Close chatbot"
              className="p-1 hover:bg-blue-500 rounded"
            >
              <FaTimes />
            </button>
          </div>
          <div className="flex-1 p-3 overflow-y-auto">
            {/* Placeholder: replace with actual AI chat integration */}
            <p className="text-sm text-gray-700">
              Bonjour ! Je suis là pour aider. Comment puis-je vous assister ?
            </p>
          </div>
          <div className="p-2 bg-gray-100">
            <input
              type="text"
              placeholder="Tapez un message..."
              aria-label="Type your message"
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>
      )}

      <button
        onClick={() => setOpen(prev => !prev)}
        aria-label="Toggle chatbot"
        className="bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        <FaComments size={20} />
      </button>
    </div>
  );
};

export default ChatbotWidget;
