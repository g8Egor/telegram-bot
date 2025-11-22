import { motion } from "motion/react";
import { dataStorage } from "./lib/dataStorage";
import { getIconComponent } from "./utils/iconLoader";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation, getTranslatedArray } from "./utils/i18n";

export function AboutSection() {
  const { language } = useLanguage();
  const aboutData = dataStorage.getAbout();

  return (
    <section className="py-32 px-6 bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl mb-6 tracking-tight">
            {getTranslation(aboutData.title, language)}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(aboutData.description, language)}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-12 mb-20">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-6"
          >
            <h3 className="text-3xl tracking-tight">{getTranslation(aboutData.whoWeAre.title, language)}</h3>
            {aboutData.whoWeAre.paragraphs.map((paragraph, idx) => (
              <p key={idx} className="text-lg text-gray-600 leading-relaxed">
                {getTranslation(paragraph, language)}
              </p>
            ))}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-6"
          >
            <h3 className="text-3xl tracking-tight">{getTranslation(aboutData.goals.title, language)}</h3>
            <ul className="space-y-4">
              {aboutData.goals.items.map((goal, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-600 mt-2.5 flex-shrink-0" />
                  <span className="text-lg text-gray-600">{getTranslation(goal, language)}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h3 className="text-3xl tracking-tight text-center mb-12">
            {language === "ru" ? "Наши ценности" : "Our Values"}
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {aboutData.values.map((value, index) => {
              const IconComponent = getIconComponent(value.icon);
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-6">
                    <IconComponent className="w-6 h-6 text-blue-600" />
                  </div>
                  <h4 className="text-xl mb-3">{getTranslation(value.title, language)}</h4>
                  <p className="text-gray-600">{getTranslation(value.description, language)}</p>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
