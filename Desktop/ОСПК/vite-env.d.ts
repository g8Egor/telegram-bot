/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_ADMIN_PASSWORD?: string;
  // добавьте другие переменные окружения здесь по мере необходимости
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

