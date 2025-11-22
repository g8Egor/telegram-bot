// Утилита для работы с данными (localStorage для демо, можно заменить на API)
import { 
  heroData, 
  aboutData, 
  membershipData, 
  newsData, 
  teamData, 
  documentsData, 
  galleryData, 
  contactsData, 
  footerData 
} from '../data';
import type {
  HeroData,
  AboutData,
  MembershipData,
  NewsData,
  TeamData,
  DocumentsData,
  GalleryData,
  ContactsData,
  FooterData,
} from '../data/types';

const STORAGE_PREFIX = 'ospk_data_';

// Функция для загрузки данных из localStorage или возврата дефолтных
function loadData<T>(key: string, defaultData: T): T {
  if (typeof window === 'undefined') return defaultData;
  
  try {
    const stored = localStorage.getItem(STORAGE_PREFIX + key);
    if (stored) {
      return JSON.parse(stored) as T;
    }
  } catch (error) {
    console.error(`Error loading ${key}:`, error);
  }
  
  return defaultData;
}

// Функция для сохранения данных в localStorage
function saveData<T>(key: string, data: T): void {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(data));
  } catch (error) {
    console.error(`Error saving ${key}:`, error);
  }
}

// API для работы с данными
export const dataStorage = {
  // Hero
  getHero: () => loadData<HeroData>('hero', heroData),
  saveHero: (data: HeroData) => saveData('hero', data),
  
  // About
  getAbout: () => loadData<AboutData>('about', aboutData),
  saveAbout: (data: AboutData) => saveData('about', data),
  
  // Memberships
  getMemberships: () => loadData<MembershipData>('memberships', membershipData),
  saveMemberships: (data: MembershipData) => saveData('memberships', data),
  
  // News
  getNews: () => loadData<NewsData>('news', newsData),
  saveNews: (data: NewsData) => saveData('news', data),
  
  // Team
  getTeam: () => loadData<TeamData>('team', teamData),
  saveTeam: (data: TeamData) => saveData('team', data),
  
  // Documents
  getDocuments: () => loadData<DocumentsData>('documents', documentsData),
  saveDocuments: (data: DocumentsData) => saveData('documents', data),
  
  // Gallery
  getGallery: () => loadData<GalleryData>('gallery', galleryData),
  saveGallery: (data: GalleryData) => saveData('gallery', data),
  
  // Contacts
  getContacts: () => loadData<ContactsData>('contacts', contactsData),
  saveContacts: (data: ContactsData) => saveData('contacts', data),
  
  // Footer
  getFooter: () => loadData<FooterData>('footer', footerData),
  saveFooter: (data: FooterData) => saveData('footer', data),
};

// TODO: Для продакшена заменить на реальные API вызовы:
// Пример:
// export const dataStorage = {
//   getHero: async () => {
//     const response = await fetch('/api/data/hero');
//     return response.json();
//   },
//   saveHero: async (data: HeroData) => {
//     await fetch('/api/data/hero', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(data),
//     });
//   },
//   // ... остальные методы
// };

