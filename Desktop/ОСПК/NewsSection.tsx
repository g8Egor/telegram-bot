import { motion } from "motion/react";
import { Calendar } from "lucide-react";
import { ImageWithFallback } from "./components/figma/ImageWithFallback";
import { dataStorage } from "./lib/dataStorage";
import { useState } from "react";
import { LegalModal } from "./LegalModal";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";
import { commonTranslations } from "./i18n/common";
import type { NewsItem } from "./data/types";

export function NewsSection() {
  const { language } = useLanguage();
  const newsData = dataStorage.getNews();
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleReadMore = (item: NewsItem) => {
    setSelectedNews(item);
    setIsModalOpen(true);
  };

  return (
    <section className="py-32 px-6 bg-white">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl mb-6 tracking-tight">
            {getTranslation(newsData.title, language)}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(newsData.description, language)}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {newsData.items.map((item, index) => (
            <motion.article
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="group bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-shadow duration-500"
            >
              <div className="aspect-[16/10] overflow-hidden bg-gray-100">
                <ImageWithFallback
                  src={item.image}
                  alt={getTranslation(item.title, language)}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                />
              </div>
              <div className="p-8 space-y-4">
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Calendar size={16} />
                  <time>{item.date}</time>
                </div>
                <h3 className="text-2xl tracking-tight group-hover:text-blue-600 transition-colors">
                  {getTranslation(item.title, language)}
                </h3>
                <p className="text-gray-600 leading-relaxed">{getTranslation(item.excerpt, language)}</p>
                <button 
                  onClick={() => handleReadMore(item)}
                  className="text-blue-600 hover:text-blue-700 transition-colors inline-flex items-center gap-1"
                >
                  {getTranslation(commonTranslations.readMore, language)}
                  <span className="group-hover:translate-x-1 transition-transform">→</span>
                </button>
              </div>
            </motion.article>
          ))}
        </div>
      </div>

      {/* News Modal */}
      {selectedNews && (
        <LegalModal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedNews(null);
          }}
          type="news"
          newsContent={{
            title: getTranslation(selectedNews.title, language),
            content: getTranslation(selectedNews.content || selectedNews.excerpt, language),
          }}
        />
      )}
    </section>
  );
}
