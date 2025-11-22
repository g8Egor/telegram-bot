import { motion } from "motion/react";
import { FileText, Download } from "lucide-react";
import { Button } from "./components/ui/button";
import { dataStorage } from "./lib/dataStorage";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";
import { commonTranslations } from "./i18n/common";

export function DocumentsSection() {
  const { language } = useLanguage();
  const documentsData = dataStorage.getDocuments();
  const handleDownload = (title: string) => {
    console.log(`Downloading: ${title}`);
    // В реальном приложении здесь была бы логика скачивания файла
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
            {getTranslation(documentsData.title, language)}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(documentsData.description, language)}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6">
          {documentsData.items.map((doc, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.05 }}
              className="group bg-white border border-gray-200 rounded-2xl p-6 hover:border-blue-200 hover:shadow-lg transition-all duration-300"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0 group-hover:bg-blue-100 transition-colors">
                  <FileText className="w-6 h-6 text-blue-600" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <h3 className="text-xl tracking-tight">{getTranslation(doc.title, language)}</h3>
                    <span className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-md flex-shrink-0">
                      {doc.type}
                    </span>
                  </div>
                  
                  <p className="text-gray-600 mb-4">{getTranslation(doc.description, language)}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-500 space-y-1">
                      <div>{doc.size}</div>
                      <div>{doc.date}</div>
                    </div>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDownload(doc.title)}
                      className="gap-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
                    >
                      <Download size={16} />
                      {getTranslation(commonTranslations.download, language)}
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}