import { motion } from "motion/react";
import { Mail, Linkedin } from "lucide-react";
import { dataStorage } from "./lib/dataStorage";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";

export function TeamSection() {
  const { language } = useLanguage();
  const teamData = dataStorage.getTeam();
  const handleMailClick = (email?: string) => {
    if (email) {
      window.location.href = `mailto:${email}`;
    } else {
      console.log("Email clicked");
    }
  };

  const handleLinkedInClick = () => {
    console.log("LinkedIn clicked");
  };

  const handleVacanciesClick = () => {
    const element = document.getElementById("contacts");
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
            {getTranslation(teamData.title, language)}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(teamData.description, language)}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {teamData.members.map((member, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.05 }}
              className="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-xl transition-all duration-500 text-center"
            >
              <div className="mb-6">
                <div className={`w-24 h-24 mx-auto rounded-full bg-gradient-to-br ${member.color} flex items-center justify-center text-white text-2xl mb-4 group-hover:scale-105 transition-transform duration-300`}>
                  {member.initials}
                </div>
              </div>

              <h3 className="text-xl mb-2 tracking-tight">{getTranslation(member.name, language)}</h3>
              <p className="text-blue-600 mb-2">{getTranslation(member.role, language)}</p>
              <p className="text-sm text-gray-600 mb-6">{getTranslation(member.specialty, language)}</p>

              <div className="flex items-center justify-center gap-3 pt-4 border-t border-gray-100">
                <button 
                  onClick={() => handleMailClick()}
                  className="w-9 h-9 rounded-full bg-gray-100 hover:bg-blue-50 flex items-center justify-center transition-colors group/btn"
                >
                  <Mail size={16} className="text-gray-600 group-hover/btn:text-blue-600" />
                </button>
                <button 
                  onClick={handleLinkedInClick}
                  className="w-9 h-9 rounded-full bg-gray-100 hover:bg-blue-50 flex items-center justify-center transition-colors group/btn"
                >
                  <Linkedin size={16} className="text-gray-600 group-hover/btn:text-blue-600" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="mt-16 text-center"
        >
          <p className="text-lg text-gray-600 mb-6">
            {getTranslation(teamData.vacanciesText, language)}
          </p>
          <button 
            onClick={handleVacanciesClick}
            className="text-blue-600 hover:text-blue-700 transition-colors inline-flex items-center gap-2"
          >
            {getTranslation(teamData.vacanciesButtonText, language)}
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </button>
        </motion.div>
      </div>
    </section>
  );
}
