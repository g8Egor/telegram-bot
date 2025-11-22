import { motion, AnimatePresence } from "motion/react";
import { X } from "lucide-react";
import { useLanguage } from "./contexts/LanguageContext";
import { legalTranslations } from "./i18n/legal";

interface LegalModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: "privacy" | "data-processing" | "news";
  newsContent?: {
    title: string;
    content: string;
  };
}

export function LegalModal({ isOpen, onClose, type, newsContent }: LegalModalProps) {
  const { language } = useLanguage();
  
  const formatLegalContent = (text: string) => {
    return text.split('\n\n').map((paragraph, index) => {
      const trimmed = paragraph.trim();
      if (!trimmed) return null;
      
      if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
        const items = trimmed.split('\n').filter(item => item.trim());
        return (
          <ul key={index} className="list-disc list-inside mb-4 space-y-2 ml-4">
            {items.map((item, itemIndex) => (
              <li key={itemIndex} className="mb-2">{item.replace(/^[•\-]\s*/, '')}</li>
            ))}
          </ul>
        );
      }
      
      if (trimmed.match(/^\d+\./)) {
        return <p key={index} className="mb-4">{trimmed}</p>;
      }
      
      if (trimmed.match(/^\d+\.\s+[А-ЯA-Z]/)) {
        return <h3 key={index} className="text-xl mb-3 mt-6">{trimmed}</h3>;
      }
      
      return <p key={index} className="mb-4">{trimmed}</p>;
    });
  };

  const content = {
    privacy: {
      title: legalTranslations.privacy.title[language],
      text: <div className="prose prose-gray max-w-none">{formatLegalContent(legalTranslations.privacy.content[language])}</div>,
    },
    "data-processing": {
      title: legalTranslations.dataProcessing.title[language],
      text: <div className="prose prose-gray max-w-none">{formatLegalContent(legalTranslations.dataProcessing.content[language])}</div>,
    },
    news: {
      title: newsContent?.title || (language === "ru" ? "Новость" : "News"),
      text: newsContent?.content && newsContent.content.trim() ? (
        <div className="prose prose-gray max-w-none">
          {newsContent.content.split('\n\n').map((paragraph, index) => {
            const trimmed = paragraph.trim();
            if (!trimmed) return null;
            
            if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
              const items = trimmed.split('\n').filter(item => item.trim());
              return (
                <ul key={index} className="list-disc list-inside mb-4 space-y-2 ml-4">
                  {items.map((item, itemIndex) => (
                    <li key={itemIndex} className="mb-2">{item.replace(/^[•\-]\s*/, '')}</li>
                  ))}
          </ul>
              );
            }
            
            return (
              <p key={index} className="mb-4 leading-relaxed">{trimmed}</p>
            );
          })}
        </div>
      ) : (
        <p className="text-gray-600">{language === "ru" ? "Контент новости отсутствует" : "News content is missing"}</p>
      ),
    },
  };

  const selectedContent = type === "news" && newsContent 
    ? content.news 
    : content[type as "privacy" | "data-processing"];

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{ duration: 0.2 }}
              className="bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[85vh] overflow-hidden pointer-events-auto"
            >
              {/* Header */}
              <div className="flex items-center justify-between px-8 py-6 border-b border-gray-100">
                <h2 className="text-2xl tracking-tight">
                  {selectedContent.title}
                </h2>
                <button
                  onClick={onClose}
                  className="w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors"
                >
                  <X size={20} />
                </button>
              </div>

              {/* Content */}
              <div className="px-8 py-6 overflow-y-auto max-h-[calc(85vh-88px)]">
                <div className="text-gray-700 leading-relaxed">
                  {selectedContent.text}
                </div>
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
