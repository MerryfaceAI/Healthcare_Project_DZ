// src/utils/theme.ts

export function applyTheme(name: 'theme-light' | 'theme-dark' | 'theme-sober') {
  document.documentElement.className = name;
  localStorage.setItem('theme', name);
}

export function loadTheme(): 'theme-light' | 'theme-dark' | 'theme-sober' {
  return (localStorage.getItem('theme') as any) || 'theme-light';
}
export function toggleTheme() {
  const currentTheme = loadTheme();
  if (currentTheme === 'theme-light') {
    applyTheme('theme-dark');
  } else if (currentTheme === 'theme-dark') {
    applyTheme('theme-sober');
  } else {
    applyTheme('theme-light');
  }
}