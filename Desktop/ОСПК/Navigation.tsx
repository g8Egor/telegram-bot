import { motion } from "motion/react";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { useLanguage } from "./contexts/LanguageContext";
import { navigationTranslations } from "./i18n/navigation";
import { getTranslation } from "./utils/i18n";

interface NavigationProps {
  activeSection: string;
  onNavigate: (section: string) => void;
}

export function Navigation({ activeSection, onNavigate }: NavigationProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { language, setLanguage } = useLanguage();

  const navItems = [
    { id: "home", label: navigationTranslations.home },
    { id: "about", label: navigationTranslations.about },
    { id: "membership", label: navigationTranslations.membership },
    { id: "team", label: navigationTranslations.team },
    { id: "documents", label: navigationTranslations.documents },
    { id: "news", label: navigationTranslations.news },
    { id: "gallery", label: navigationTranslations.gallery },
    { id: "contacts", label: navigationTranslations.contacts },
  ];

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.button
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={scrollToTop}
            className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity"
          >
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-blue-400" />
            <span className="text-lg tracking-tight">ОСПК</span>
          </motion.button>

          {/* Desktop Navigation - Centered */}
          <div className="hidden lg:flex items-center justify-center flex-1 mx-12">
            <div className="flex items-center gap-6">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`relative py-2 px-1 transition-colors whitespace-nowrap ${
                    activeSection === item.id
                      ? "text-blue-600"
                      : "text-gray-600 hover:text-gray-900"
                  }`}
                >
                  {getTranslation(item.label, language)}
                  {activeSection === item.id && (
                    <motion.div
                      layoutId="activeSection"
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Language Switcher */}
          <div className="hidden lg:flex items-center gap-2">
            <button
              onClick={() => setLanguage("ru")}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                language === "ru"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              RU
            </button>
            <span className="text-gray-300">|</span>
            <button
              onClick={() => setLanguage("en")}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                language === "en"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              EN
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden p-2"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden pt-4 pb-2"
          >
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left py-3 px-4 rounded-lg transition-colors ${
                  activeSection === item.id
                    ? "bg-blue-50 text-blue-600"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                {getTranslation(item.label, language)}
              </button>
            ))}
            {/* Language Switcher in Mobile Menu */}
            <div className="flex items-center justify-center gap-2 pt-4 border-t border-gray-200 mt-2">
              <button
                onClick={() => setLanguage("ru")}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  language === "ru"
                    ? "bg-blue-600 text-white"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                RU
              </button>
              <span className="text-gray-300">|</span>
              <button
                onClick={() => setLanguage("en")}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  language === "en"
                    ? "bg-blue-600 text-white"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                EN
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </nav>
  );
}