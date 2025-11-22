// Общие типы данных для всего проекта

// Базовый тип для переводимых строк
export interface TranslatedString {
  ru: string;
  en: string;
}

export interface HeroData {
  badge: TranslatedString;
  title: TranslatedString;
  description: TranslatedString;
  buttonText: TranslatedString;
  backgroundImage: string; // URL не переводится
}

export interface Value {
  icon: string; // Название иконки из lucide-react
  title: TranslatedString;
  description: TranslatedString;
}

export interface AboutData {
  title: TranslatedString;
  description: TranslatedString;
  whoWeAre: {
    title: TranslatedString;
    paragraphs: TranslatedString[];
  };
  goals: {
    title: TranslatedString;
    items: TranslatedString[];
  };
  values: Value[];
}

export interface MembershipCategory {
  id: string;
  title: TranslatedString;
  price: string; // Цена обычно не переводится, но может быть форматирована
  description: TranslatedString;
  features: TranslatedString[];
  color: string; // Tailwind классы для градиента
  icon: string; // Название иконки из lucide-react
}

export interface MembershipData {
  title: TranslatedString;
  description: TranslatedString;
  categories: MembershipCategory[];
  formTitle: TranslatedString;
  formDescription: TranslatedString;
  submitButtonText: TranslatedString;
  submitMessage: TranslatedString;
}

export interface NewsItem {
  id: string;
  title: TranslatedString;
  date: string; // Дата может быть отформатирована по-разному, но пока оставим строкой
  excerpt: TranslatedString; // Краткое описание для карточки
  image: string; // URL не переводится
  content: TranslatedString; // Полный текст новости для попапа "Читать далее"
}

export interface NewsData {
  title: TranslatedString;
  description: TranslatedString;
  items: NewsItem[];
}

export interface TeamMember {
  id: string;
  name: TranslatedString;
  role: TranslatedString;
  specialty: TranslatedString;
  initials: string; // Инициалы обычно не меняются
  color: string; // Tailwind классы для градиента
  email?: string;
  linkedin?: string;
}

export interface TeamData {
  title: TranslatedString;
  description: TranslatedString;
  members: TeamMember[];
  vacanciesText: TranslatedString;
  vacanciesButtonText: TranslatedString;
}

export interface Document {
  id: string;
  title: TranslatedString;
  description: TranslatedString;
  size: string; // Размер файла обычно не переводится
  date: string; // Дата
  type: string; // PDF, DOCX и т.д. - обычно не переводится
  fileUrl?: string; // URL для скачивания
}

export interface DocumentsData {
  title: TranslatedString;
  description: TranslatedString;
  items: Document[];
}

export interface GalleryImage {
  id: string;
  url: string; // URL не переводится
  title: TranslatedString;
  description: TranslatedString;
}

export interface GalleryData {
  title: TranslatedString;
  description: TranslatedString;
  images: GalleryImage[];
}

export interface ContactInfo {
  id: string;
  icon: string; // Название иконки из lucide-react
  label: TranslatedString;
  value: string; // Контактные данные обычно не переводится
  href: string | null;
}

export interface ContactsData {
  title: TranslatedString;
  description: TranslatedString;
  contactTitle: TranslatedString;
  contactDescription: TranslatedString;
  contactInfo: ContactInfo[];
  formTitle: TranslatedString;
  formNameLabel: TranslatedString;
  formEmailLabel: TranslatedString;
  formMessageLabel: TranslatedString;
  formSubmitText: TranslatedString;
  formResponseTime: TranslatedString;
}

export interface FooterLink {
  label: TranslatedString;
  href: string; // URL не переводится
}

export interface FooterData {
  organizationName: TranslatedString;
  description: TranslatedString;
  email: string; // Email не переводится
  phone: string; // Телефон не переводится
  links: {
    about: FooterLink[];
    services: FooterLink[];
    resources: FooterLink[];
  };
  copyright: TranslatedString;
}
