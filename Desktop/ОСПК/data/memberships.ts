import { MembershipData } from './types';

export const membershipData: MembershipData = {
  title: {
    ru: "Вступление в членство",
    en: "Membership",
  },
  description: {
    ru: "Станьте частью профессионального сообщества психологов",
    en: "Become part of a professional community of psychologists",
  },
  categories: [
    {
      id: "full-member",
      title: {
        ru: "Действительный член",
        en: "Full Member",
      },
      price: "15 000 ₽",
      description: {
        ru: "Для практикующих психологов с высшим психологическим образованием",
        en: "For practicing psychologists with higher psychological education",
      },
      features: [
        {
          ru: "Полный доступ ко всем ресурсам сообщества",
          en: "Full access to all community resources",
        },
        {
          ru: "Участие в голосовании и принятии решений",
          en: "Participation in voting and decision-making",
        },
        {
          ru: "Возможность участия в проектах",
          en: "Opportunity to participate in projects",
        },
        {
          ru: "Супервизия и профессиональная поддержка",
          en: "Supervision and professional support",
        },
        {
          ru: "Сертификат члена ОСПК",
          en: "OSPK member certificate",
        },
      ],
      color: "from-blue-500 to-blue-600",
      icon: "GraduationCap",
    },
    {
      id: "associate-member",
      title: {
        ru: "Ассоциированный член",
        en: "Associate Member",
      },
      price: "8 000 ₽",
      description: {
        ru: "Для специалистов смежных профессий и студентов психологических факультетов",
        en: "For specialists in related professions and students of psychology faculties",
      },
      features: [
        {
          ru: "Доступ к образовательным материалам",
          en: "Access to educational materials",
        },
        {
          ru: "Участие в мероприятиях",
          en: "Participation in events",
        },
        {
          ru: "Консультации и поддержка",
          en: "Consultations and support",
        },
        {
          ru: "Возможность перехода в действительные члены",
          en: "Opportunity to transition to full membership",
        },
      ],
      color: "from-purple-500 to-purple-600",
      icon: "Users",
    },
    {
      id: "honorary-member",
      title: {
        ru: "Почётный член",
        en: "Honorary Member",
      },
      price: "Без взноса",
      description: {
        ru: "По решению правления за особый вклад в развитие психологии",
        en: "By decision of the board for special contribution to the development of psychology",
      },
      features: [
        {
          ru: "Все права действительного члена",
          en: "All rights of a full member",
        },
        {
          ru: "Участие в экспертных советах",
          en: "Participation in expert councils",
        },
        {
          ru: "Менторство молодых специалистов",
          en: "Mentoring young specialists",
        },
        {
          ru: "Приглашения на закрытые мероприятия",
          en: "Invitations to closed events",
        },
      ],
      color: "from-amber-500 to-amber-600",
      icon: "Award",
    },
  ],
  formTitle: {
    ru: "Анкета для вступления",
    en: "Membership Application Form",
  },
  formDescription: {
    ru: "Заполните анкету, и мы свяжемся с вами в ближайшее время",
    en: "Fill out the form and we will contact you soon",
  },
  submitButtonText: {
    ru: "Отправить заявку",
    en: "Submit Application",
  },
  submitMessage: {
    ru: "После отправки заявки мы свяжемся с вами для дальнейших шагов",
    en: "After submitting the application, we will contact you for further steps",
  },
};
