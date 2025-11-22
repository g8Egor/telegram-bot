// Простая система аутентификации для админ-панели
// Использует localStorage для хранения сессии

const ADMIN_SESSION_KEY = 'ospk_admin_session';

// Получить пароль из переменных окружения или использовать дефолтный
function getAdminPassword(): string {
  // В Vite переменные окружения доступны через import.meta.env
  const envPassword = import.meta.env.VITE_ADMIN_PASSWORD;
  return envPassword || 'admin123'; // Дефолтный пароль для разработки
}

export const auth = {
  // Проверка пароля и создание сессии
  login: (password: string): boolean => {
    const correctPassword = getAdminPassword();
    
    if (password === correctPassword) {
      const session = {
        authenticated: true,
        timestamp: Date.now(),
        expiresAt: Date.now() + 24 * 60 * 60 * 1000, // 24 часа
      };
      localStorage.setItem(ADMIN_SESSION_KEY, JSON.stringify(session));
      return true;
    }
    
    return false;
  },
  
  // Проверка, авторизован ли пользователь
  isAuthenticated: (): boolean => {
    if (typeof window === 'undefined') return false;
    
    try {
      const sessionStr = localStorage.getItem(ADMIN_SESSION_KEY);
      if (!sessionStr) return false;
      
      const session = JSON.parse(sessionStr);
      
      // Проверка срока действия сессии
      if (Date.now() > session.expiresAt) {
        localStorage.removeItem(ADMIN_SESSION_KEY);
        return false;
      }
      
      return session.authenticated === true;
    } catch {
      return false;
    }
  },
  
  // Выход из системы
  logout: (): void => {
    localStorage.removeItem(ADMIN_SESSION_KEY);
  },
};

