import { GalleryData } from './types';

export const galleryData: GalleryData = {
  title: {
    ru: "Фотогалерея",
    en: "Photo Gallery",
  },
  description: {
    ru: "Моменты из жизни нашего профессионального сообщества",
    en: "Moments from the life of our professional community",
  },
  images: [
    {
      id: "gallery-1",
      url: "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=800&q=80",
      title: {
        ru: "Конференция 2024",
        en: "Conference 2024",
      },
      description: {
        ru: "Ежегодная конференция психологов",
        en: "Annual psychologists conference",
      },
    },
    {
      id: "gallery-2",
      url: "https://images.unsplash.com/photo-1560439514-4e9645039924?w=800&q=80",
      title: {
        ru: "Круглый стол",
        en: "Round Table",
      },
      description: {
        ru: "Обсуждение методик и подходов",
        en: "Discussion of methods and approaches",
      },
    },
    {
      id: "gallery-3",
      url: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=800&q=80",
      title: {
        ru: "Образовательный семинар",
        en: "Educational Seminar",
      },
      description: {
        ru: "Повышение квалификации специалистов",
        en: "Professional development of specialists",
      },
    },
  ],
};
