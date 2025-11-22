import { motion } from "motion/react";
import { Button } from "./components/ui/button";
import { ArrowRight } from "lucide-react";
import { ImageWithFallback } from "./components/figma/ImageWithFallback";
import { dataStorage } from "./lib/dataStorage";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";

export function HeroSection() {
  const { language } = useLanguage();
  const heroData = dataStorage.getHero();
  const handleJoinClick = () => {
    const element = document.getElementById("membership");
    if (element) {
      const offset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;
      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth",
      });
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center pt-20 px-6 overflow-hidden">
      {/* Background Image with Opacity */}
      <div className="absolute inset-0 z-0">
        <ImageWithFallback
          src={heroData.backgroundImage}
          alt="Психологическое консультирование"
          className="w-full h-full object-cover opacity-15"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-white/60 via-white/80 to-white" />
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto w-full relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.25, 0.1, 0.25, 1] }}
          className="text-center space-y-8"
        >
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-block px-4 py-2 bg-blue-50 text-blue-600 rounded-full"
          >
            {getTranslation(heroData.badge, language)}
          </motion.div>
          
          <h1 className="text-5xl md:text-6xl lg:text-7xl tracking-tight leading-tight">
            {getTranslation(heroData.title, language)}
          </h1>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(heroData.description, language)}
          </p>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Button
              size="lg"
              onClick={handleJoinClick}
              className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 py-6 gap-2 shadow-lg shadow-blue-600/20"
            >
              {getTranslation(heroData.buttonText, language)}
              <ArrowRight size={20} />
            </Button>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}