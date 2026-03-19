export type Theme = 'light' | 'dark';

export const applyTheme = (theme: Theme) => {
  const root = window.document.documentElement;
  root.classList.remove('light', 'dark');
  root.classList.add(theme);
  // Saves preference so it persists after refresh
  localStorage.setItem('app-theme', theme);
};

export const getSavedTheme = (): Theme => {
  const saved = localStorage.getItem('app-theme') as Theme;
  if (saved) return saved;
  // Defaults to system preference if no manual choice exists
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};
