import { Link } from "react-router-dom";
import { motion } from "motion/react";
import { 
  FileText, 
  Users, 
  Newspaper, 
  Image, 
  Mail, 
  Settings, 
  LogOut,
  GraduationCap,
  FolderOpen,
  Home
} from "lucide-react";
import { auth } from "../lib/auth";
import { useNavigate } from "react-router-dom";
import { dataStorage } from "../lib/dataStorage";
import { useLanguage } from "../contexts/LanguageContext";
import { adminTranslations } from "../i18n/admin";
import { getTranslation } from "../utils/i18n";

export function AdminDashboard() {
  const navigate = useNavigate();
  const { language } = useLanguage();

  const handleLogout = () => {
    auth.logout();
    navigate("/admin/login");
  };

  const sections = [
    {
      id: "hero",
      title: getTranslation(adminTranslations.heroPage, language),
      description: language === "ru" ? "Заголовок, описание, кнопка" : "Title, description, button",
      icon: Home,
      count: "1",
      color: "bg-blue-500",
      path: "/admin/settings",
    },
    {
      id: "about",
      title: getTranslation(adminTranslations.aboutSection, language),
      description: language === "ru" ? "Тексты, ценности, цели" : "Texts, values, goals",
      icon: FileText,
      count: `${dataStorage.getAbout().values.length} ${language === "ru" ? "ценностей" : "values"}`,
      color: "bg-green-500",
      path: "/admin/settings",
    },
    {
      id: "memberships",
      title: language === "ru" ? "Членство / Тарифы" : "Membership / Rates",
      description: language === "ru" ? "Категории членства и цены" : "Membership categories and prices",
      icon: GraduationCap,
      count: `${dataStorage.getMemberships().categories.length} ${language === "ru" ? "тарифов" : "rates"}`,
      color: "bg-purple-500",
      path: "/admin/memberships",
    },
    {
      id: "news",
      title: getTranslation(adminTranslations.newsManagement, language),
      description: getTranslation(adminTranslations.newsDescription, language),
      icon: Newspaper,
      count: `${dataStorage.getNews().items.length} ${language === "ru" ? "новостей" : "news"}`,
      color: "bg-orange-500",
      path: "/admin/news",
    },
    {
      id: "team",
      title: getTranslation(adminTranslations.teamManagement, language),
      description: getTranslation(adminTranslations.teamDescription, language),
      icon: Users,
      count: `${dataStorage.getTeam().members.length} ${language === "ru" ? "человек" : "members"}`,
      color: "bg-pink-500",
      path: "/admin/team",
    },
    {
      id: "documents",
      title: language === "ru" ? "Документы" : "Documents",
      description: language === "ru" ? "Файлы и документы для скачивания" : "Files and documents for download",
      icon: FolderOpen,
      count: `${dataStorage.getDocuments().items.length} ${language === "ru" ? "документов" : "documents"}`,
      color: "bg-indigo-500",
      path: "/admin/documents",
    },
    {
      id: "gallery",
      title: language === "ru" ? "Галерея" : "Gallery",
      description: language === "ru" ? "Фотографии и изображения" : "Photos and images",
      icon: Image,
      count: `${dataStorage.getGallery().images.length} ${language === "ru" ? "фото" : "photos"}`,
      color: "bg-teal-500",
      path: "/admin/gallery",
    },
    {
      id: "contacts",
      title: language === "ru" ? "Контакты" : "Contacts",
      description: language === "ru" ? "Контактная информация" : "Contact information",
      icon: Mail,
      count: `${dataStorage.getContacts().contactInfo.length} ${language === "ru" ? "контактов" : "contacts"}`,
      color: "bg-red-500",
      path: "/admin/contacts",
    },
    {
      id: "footer",
      title: getTranslation(adminTranslations.footer, language),
      description: language === "ru" ? "Нижняя часть сайта" : "Bottom section of the site",
      icon: Settings,
      count: getTranslation(adminTranslations.settings, language),
      color: "bg-gray-500",
      path: "/admin/settings",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{getTranslation(adminTranslations.dashboard, language)}</h1>
            <p className="text-sm text-gray-600">{language === "ru" ? "Управление контентом сайта" : "Site content management"}</p>
          </div>
          <div className="flex items-center gap-4">
            <Link
              to="/"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Home size={20} />
            </Link>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <LogOut size={18} />
              <span>{getTranslation(adminTranslations.logout, language)}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">{language === "ru" ? "Разделы управления" : "Management Sections"}</h2>
          <p className="text-gray-600">{language === "ru" ? "Выберите раздел для редактирования контента" : "Select a section to edit content"}</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sections.map((section, index) => {
            const Icon = section.icon;
            return (
              <motion.div
                key={section.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Link
                  to={section.path}
                  className="block bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-all border border-gray-200 hover:border-blue-300 group"
                >
                  <div className="flex items-start gap-4">
                    <div className={`${section.color} rounded-lg p-3 text-white group-hover:scale-110 transition-transform`}>
                      <Icon size={24} />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-1 group-hover:text-blue-600 transition-colors">
                        {section.title}
                      </h3>
                      <p className="text-sm text-gray-600 mb-3">{section.description}</p>
                      <div className="text-xs text-gray-500 font-medium">{section.count}</div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            );
          })}
        </div>

        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">{language === "ru" ? "Информация" : "Information"}</h3>
          <p className="text-sm text-blue-800">
            {language === "ru" 
              ? "Все изменения сохраняются в localStorage браузера. Для продакшена необходимо подключить реальный API или базу данных."
              : "All changes are saved to browser localStorage. For production, you need to connect a real API or database."}
          </p>
        </div>
      </main>
    </div>
  );
}

