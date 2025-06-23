import React from "react";
import { Link } from "react-router-dom";

const NotFound: React.FC = () => (
  <div className="h-full flex flex-col items-center justify-center p-6">
    <h1 className="text-4xl font-bold mb-4">404 − Page Not Found</h1>
    <p className="text-gray-600 mb-6">
      Sorry, we couldn’t find the page you’re looking for.
    </p>
    <Link
      to="/dashboard"
      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
    >
      Go to Dashboard
    </Link>
  </div>
);

export default NotFound;
