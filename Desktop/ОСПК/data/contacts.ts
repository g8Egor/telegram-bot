import { ContactsData } from './types';

export const contactsData: ContactsData = {
  title: {
    ru: "Контакты",
    en: "Contacts",
  },
  description: {
    ru: "Свяжитесь с нами для получения дополнительной информации или консультации",
    en: "Contact us for additional information or consultation",
  },
  contactTitle: {
    ru: "Свяжитесь с нами",
    en: "Contact Us",
  },
  contactDescription: {
    ru: "Мы всегда рады ответить на ваши вопросы и помочь с любыми запросами. Выберите удобный способ связи или заполните форму обратной связи.",
    en: "We are always happy to answer your questions and help with any requests. Choose a convenient way to contact us or fill out the feedback form.",
  },
  contactInfo: [
    {
      id: "contact-1",
      icon: "Mail",
      label: {
        ru: "Email",
        en: "Email",
      },
      value: "info@ospk.org",
      href: "mailto:info@ospk.org",
    },
    {
      id: "contact-2",
      icon: "Phone",
      label: {
        ru: "Телефон",
        en: "Phone",
      },
      value: "+7 (495) 123-45-67",
      href: "tel:+74951234567",
    },
    {
      id: "contact-3",
      icon: "MapPin",
      label: {
        ru: "Адрес",
        en: "Address",
      },
      value: "Москва, ул. Примерная, д. 123",
      href: null,
    },
  ],
  formTitle: {
    ru: "Напишите нам",
    en: "Write to Us",
  },
  formNameLabel: {
    ru: "Ваше имя",
    en: "Your Name",
  },
  formEmailLabel: {
    ru: "Email",
    en: "Email",
  },
  formMessageLabel: {
    ru: "Сообщение",
    en: "Message",
  },
  formSubmitText: {
    ru: "Отправить сообщение",
    en: "Send Message",
  },
  formResponseTime: {
    ru: "Мы ответим вам в течение 24 часов в рабочие дни",
    en: "We will respond within 24 hours on business days",
  },
};
