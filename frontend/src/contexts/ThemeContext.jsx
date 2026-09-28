import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const DEFAULT_PREFERENCES = {
  theme: 'dark', // 'dark', 'light', 'system'
  accent: 'cyan', // 'cyan', 'blue', 'purple', 'green'
  glassmorphism: true,
  glow: true,
  compactSidebar: false
};

export function ThemeProvider({ children }) {
  const [preferences, setPreferences] = useState(() => {
    try {
      const saved = localStorage.getItem('phishguard_ui_prefs');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && typeof parsed === 'object') {
          return { ...DEFAULT_PREFERENCES, ...parsed };
        }
      }
    } catch (e) {
      console.error("Failed to load preferences", e);
    }
    return DEFAULT_PREFERENCES;
  });

  useEffect(() => {
    // Save to localStorage
    localStorage.setItem('phishguard_ui_prefs', JSON.stringify(preferences));
    
    // Apply theme
    const applyTheme = () => {
      const root = document.documentElement;
      const isDark = 
        preferences.theme === 'dark' || 
        (preferences.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
      
      root.dataset.theme = isDark ? 'dark' : 'light';
      root.dataset.accent = preferences.accent;
      root.dataset.glassmorphism = preferences.glassmorphism;
      root.dataset.glow = preferences.glow;
      root.dataset.compactSidebar = preferences.compactSidebar;
      
      // Update body dataset for background image
      document.body.dataset.theme = isDark ? 'dark' : 'light';
    };

    applyTheme();
    
    // Listen for system theme changes if using system theme
    if (preferences.theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => applyTheme();
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [preferences]);

  const updatePreference = (key, value) => {
    setPreferences(prev => ({ ...prev, [key]: value }));
  };

  const resetPreferences = () => {
    setPreferences(DEFAULT_PREFERENCES);
  };

  return (
    <ThemeContext.Provider value={{ preferences, updatePreference, resetPreferences }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
