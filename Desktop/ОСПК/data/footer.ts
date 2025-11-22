import { FooterData } from './types';

export const footerData: FooterData = {
  organizationName: {
    ru: "ОСПК",
    en: "OSPK",
  },
  description: {
    ru: "Объединённое сообщество психологического консультирования — профессиональная платформа для развития и поддержки психологов",
    en: "United Community of Psychological Counseling — a professional platform for the development and support of psychologists",
  },
  email: "info@ospk.org",
  phone: "+74951234567",
  links: {
    about: [
      {
        label: {
          ru: "О сообществе",
          en: "About",
        },
        href: "#about",
      },
      {
        label: {
          ru: "Миссия и ценности",
          en: "Mission and Values",
        },
        href: "#about",
      },
      {
        label: {
          ru: "История",
          en: "History",
        },
        href: "#about",
      },
    ],
    services: [
      {
        label: {
          ru: "Вступление",
          en: "Membership",
        },
        href: "#membership",
      },
      {
        label: {
          ru: "Фотогалерея",
          en: "Gallery",
        },
        href: "#gallery",
      },
      {
        label: {
          ru: "Команда",
          en: "Team",
        },
        href: "#team",
      },
    ],
    resources: [
      {
        label: {
          ru: "Документы",
          en: "Documents",
        },
        href: "#documents",
      },
      {
        label: {
          ru: "Новости",
          en: "News",
        },
        href: "#news",
      },
      {
        label: {
          ru: "Контакты",
          en: "Contacts",
        },
        href: "#contacts",
      },
    ],
  },
  copyright: {
    ru: "© 2024 ОСПК. Все права защищены.",
    en: "© 2024 OSPK. All rights reserved.",
  },
};
