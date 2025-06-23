// src/context/ThemeContext.tsx
import React, { createContext, useState, useEffect, ReactNode } from 'react';

export type Theme = 'theme-light' | 'theme-dark' | 'theme-sober';

interface ThemeContextProps {
  theme: Theme;
  setTheme: (newTheme: Theme) => void;
}

export const ThemeContext = createContext<ThemeContextProps>({
  theme: 'theme-light',
  setTheme: () => {},
});

interface Props {
  children: ReactNode;
}

export const ThemeProvider: React.FC<Props> = ({ children }) => {
  const [theme, setThemeState] = useState<Theme>('theme-light');

  useEffect(() => {
    // Read stored preference from localStorage (if present)
    const stored = localStorage.getItem('appTheme') as Theme | null;
    if (stored) {
      setThemeState(stored);
      document.documentElement.classList.add(stored);
    } else {
      document.documentElement.classList.add('theme-light');
    }
  }, []);

  const setTheme = (newTheme: Theme) => {
    // Remove any existing theme‐class
    document.documentElement.classList.remove('theme-light', 'theme-dark', 'theme-sober');
    document.documentElement.classList.add(newTheme);
    localStorage.setItem('appTheme', newTheme);
    setThemeState(newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
