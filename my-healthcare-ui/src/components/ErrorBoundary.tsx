// src/components/ErrorBoundary.tsx
import React from 'react';

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends React.Component<React.PropsWithChildren<{}>, State> {
  constructor(props: React.PropsWithChildren<{}>) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("Uncaught error in React component:", error, info);
  }

  render() {
    if (this.state.hasError && this.state.error) {
      return (
        <div className="flex items-center justify-center h-screen bg-gray-50">
          <div className="bg-white p-6 rounded-lg shadow-md max-w-md text-center">
            <h2 className="text-lg font-semibold text-red-600 mb-4">
              Something went wrong.
            </h2>
            <pre className="text-xs text-gray-700 whitespace-pre-wrap">
              {this.state.error.toString()}
            </pre>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Try Again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
