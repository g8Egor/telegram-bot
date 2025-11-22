import { motion } from "motion/react";
import { ImageWithFallback } from "./components/figma/ImageWithFallback";
import { useState } from "react";
import { X } from "lucide-react";
import { dataStorage } from "./lib/dataStorage";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";

export function GallerySection() {
  const { language } = useLanguage();
  const galleryData = dataStorage.getGallery();
  const [selectedImage, setSelectedImage] = useState<number | null>(null);

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
            {getTranslation(galleryData.title, language)}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(galleryData.description, language)}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          {galleryData.images.map((image, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="group cursor-pointer"
              onClick={() => setSelectedImage(index)}
            >
              <div className="relative aspect-[3/4] rounded-2xl overflow-hidden bg-gray-100 shadow-sm hover:shadow-xl transition-all duration-500">
                <ImageWithFallback
                  src={image.url}
                  alt={getTranslation(image.title, language)}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/0 to-black/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
                    <h3 className="text-lg mb-1">{getTranslation(image.title, language)}</h3>
                    <p className="text-sm text-gray-200">{getTranslation(image.description, language)}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Lightbox */}
        {selectedImage !== null && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-4"
            onClick={() => setSelectedImage(null)}
          >
            <button
              className="absolute top-6 right-6 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
              onClick={() => setSelectedImage(null)}
            >
              <X className="text-white" size={24} />
            </button>

            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              className="max-w-5xl w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="relative aspect-[4/3] rounded-2xl overflow-hidden">
                <ImageWithFallback
                  src={galleryData.images[selectedImage].url}
                  alt={getTranslation(galleryData.images[selectedImage].title, language)}
                  className="w-full h-full object-contain"
                />
              </div>
              <div className="text-center mt-6 text-white">
                <h3 className="text-2xl mb-2">{getTranslation(galleryData.images[selectedImage].title, language)}</h3>
                <p className="text-gray-300">{getTranslation(galleryData.images[selectedImage].description, language)}</p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </div>
    </section>
  );
}