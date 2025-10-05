import { create } from 'zustand';

interface ThemeState {
  theme: 'light' | 'dark';
  isDark: boolean;
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useThemeStore = create<ThemeState>((set) => ({
  theme: 'light',
  isDark: false,
  
  toggleTheme: () => set((state) => {
    const newTheme = state.theme === 'light' ? 'dark' : 'light';
    return { theme: newTheme, isDark: newTheme === 'dark' };
  }),
  
  setTheme: (theme: 'light' | 'dark') => set({ 
    theme, 
    isDark: theme === 'dark' 
  }),
}));
