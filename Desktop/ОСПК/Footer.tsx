import { motion } from "motion/react";
import { Mail, Phone, MapPin } from "lucide-react";
import { dataStorage } from "./lib/dataStorage";
import { useState } from "react";
import { LegalModal } from "./LegalModal";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";
import { legalTranslations } from "./i18n/legal";
import { footerTranslations } from "./i18n/footer";

export function Footer() {
  const { language } = useLanguage();
  const footerData = dataStorage.getFooter();
  const currentYear = new Date().getFullYear();
  const [legalModalType, setLegalModalType] = useState<"privacy" | "data-processing" | null>(null);

  return (
    <footer className="bg-gradient-to-b from-gray-900 to-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-12 mb-16">
          {/* Logo and Description */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="space-y-6"
            >
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600" />
                <span className="text-xl tracking-tight">{getTranslation(footerData.organizationName, language)}</span>
              </div>
              <p className="text-gray-400 max-w-sm leading-relaxed">
                {getTranslation(footerData.description, language)}
              </p>
              <div className="flex gap-4">
                <a
                  href={`mailto:${footerData.email}`}
                  className="w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                >
                  <Mail size={18} />
                </a>
                <a
                  href={`tel:${footerData.phone}`}
                  className="w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                >
                  <Phone size={18} />
                </a>
              </div>
            </motion.div>
          </div>

          {/* Links Columns */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
          >
            <h4 className="mb-4">{getTranslation(footerTranslations.about, language)}</h4>
            <ul className="space-y-3">
              {footerData.links.about.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    {getTranslation(link.label, language)}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <h4 className="mb-4">{getTranslation(footerTranslations.services, language)}</h4>
            <ul className="space-y-3">
              {footerData.links.services.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    {getTranslation(link.label, language)}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
          >
            <h4 className="mb-4">{getTranslation(footerTranslations.resources, language)}</h4>
            <ul className="space-y-3">
              {footerData.links.resources.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    {getTranslation(link.label, language)}
                  </a>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10">
          <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-500">
            <button
              onClick={(e) => {
                e.preventDefault();
                setLegalModalType("privacy");
              }}
              className="hover:text-white transition-colors cursor-pointer"
            >
              {legalTranslations.privacy.title[language]}
            </button>
            <span className="text-gray-300">•</span>
            <button
              onClick={(e) => {
                e.preventDefault();
                setLegalModalType("data-processing");
              }}
              className="hover:text-white transition-colors cursor-pointer"
            >
              {legalTranslations.dataProcessing.title[language]}
            </button>
            <span className="text-gray-300">•</span>
            <p>{getTranslation(footerData.copyright, language)}</p>
          </div>
        </div>
      </div>

      {/* Legal Modals */}
      <LegalModal
        isOpen={legalModalType === "privacy"}
        onClose={() => setLegalModalType(null)}
        type="privacy"
      />
      <LegalModal
        isOpen={legalModalType === "data-processing"}
        onClose={() => setLegalModalType(null)}
        type="data-processing"
      />
    </footer>
  );
}