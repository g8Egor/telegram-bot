import { motion } from "motion/react";
import { Check } from "lucide-react";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Textarea } from "./components/ui/textarea";
import { useState } from "react";
import { LegalModal } from "./LegalModal";
import { dataStorage } from "./lib/dataStorage";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";
import { membershipTranslations } from "./i18n/membership";

export function MembershipSection() {
  const { language } = useLanguage();
  const membershipData = dataStorage.getMemberships();
  const [modalOpen, setModalOpen] = useState<"privacy" | "data-processing" | null>(null);
  
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    phone: "",
    education: "",
    specialization: "",
    experience: "",
    category: "",
    motivation: "",
    privacyConsent: false,
    dataProcessingConsent: false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Формируем данные для отправки
    const emailBody = `
Заявка на вступление в ОСПК

ФИО: ${formData.fullName}
Email: ${formData.email}
Телефон: ${formData.phone}
Образование: ${formData.education}
Специализация: ${formData.specialization}
Опыт работы: ${formData.experience}
Категория членства: ${formData.category}
Мотивация: ${formData.motivation}
Согласие на обработку персональных данных: ${formData.dataProcessingConsent ? "Да" : "Нет"}
Согласие на обработку данных для рассылок: ${formData.privacyConsent ? "Да" : "Нет"}
    `.trim();

    // В реальном приложении здесь была бы отправка на сервер
    // Для демонстрации используем mailto
    const mailtoLink = `mailto:tanis63@list.ru?subject=${encodeURIComponent('Заявка на вступление в ОСПК')}&body=${encodeURIComponent(emailBody)}`;
    window.location.href = mailtoLink;
    
    console.log("Отправка заявки на tanis63@list.ru:", formData);
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
            {getTranslation(membershipData.title, language)}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(membershipData.description, language)}
          </p>
        </motion.div>

        {/* Категории членства */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="mb-20"
        >
          <h3 className="text-3xl tracking-tight text-center mb-12">
            {getTranslation(membershipTranslations.categoriesTitle, language)}
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            {membershipData.categories.map((category, index) => {
              return (
                <motion.div
                  key={category.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="bg-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition-all duration-500"
                >
                  <div className={`w-full h-2 rounded-t-3xl bg-gradient-to-r ${category.color} -mt-8 mb-6`} />
                  
                  <h4 className="text-2xl mb-2 tracking-tight">{getTranslation(category.title, language)}</h4>
                  <div className="text-4xl mb-4">
                    {category.price === "Без взноса" 
                      ? getTranslation(membershipTranslations.noFee, language)
                      : category.price}
                  </div>
                  <p className="text-gray-600 mb-8 leading-relaxed">
                    {getTranslation(category.description, language)}
                  </p>
                  
                  <ul className="space-y-4 mb-8">
                    {category.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start gap-3">
                        <div className="w-5 h-5 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 mt-0.5">
                          <Check size={14} className="text-blue-600" />
                        </div>
                        <span className="text-gray-700">{getTranslation(feature, language)}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              );
            })}
          </div>
        </motion.div>

        {/* Форма заявки */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl mx-auto"
        >
          <div className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-gray-100">
            <h3 className="text-3xl mb-6 tracking-tight text-center">
              {getTranslation(membershipData.formTitle, language)}
            </h3>
            <p className="text-gray-600 text-center mb-10">
              {getTranslation(membershipData.formDescription, language)}
            </p>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="fullName" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.fullName, language)} *
                  </label>
                  <Input
                    id="fullName"
                    type="text"
                    placeholder="Иванов Иван Иванович"
                    value={formData.fullName}
                    onChange={(e) =>
                      setFormData({ ...formData, fullName: e.target.value })
                    }
                    className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.email, language)} *
                  </label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="ivanov@example.com"
                    value={formData.email}
                    onChange={(e) =>
                      setFormData({ ...formData, email: e.target.value })
                    }
                    className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="phone" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.phone, language)} *
                  </label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="+7 (999) 123-45-67"
                    value={formData.phone}
                    onChange={(e) =>
                      setFormData({ ...formData, phone: e.target.value })
                    }
                    className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="category" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.category, language)} *
                  </label>
                  <select
                    id="category"
                    value={formData.category}
                    onChange={(e) =>
                      setFormData({ ...formData, category: e.target.value })
                    }
                    className="w-full rounded-xl border border-gray-200 px-4 py-2 focus:border-blue-500 focus:ring-blue-500 bg-white"
                    required
                  >
                    <option value="">{language === "ru" ? "Выберите категорию" : "Select category"}</option>
                    {membershipData.categories.map((cat) => (
                      <option key={cat.id} value={cat.id}>{getTranslation(cat.title, language)}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                  <label htmlFor="education" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.education, language)} *
                  </label>
                <Input
                  id="education"
                  type="text"
                  placeholder="ВУЗ, факультет, год окончания"
                  value={formData.education}
                  onChange={(e) =>
                    setFormData({ ...formData, education: e.target.value })
                  }
                  className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                  <label htmlFor="specialization" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.specialization, language)} *
                  </label>
                <Input
                  id="specialization"
                  type="text"
                  placeholder="Например: клиническая психология, семейная терапия"
                  value={formData.specialization}
                  onChange={(e) =>
                    setFormData({ ...formData, specialization: e.target.value })
                  }
                  className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                  <label htmlFor="experience" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.experience, language)} {language === "ru" ? "(в годах)" : "(years)"} *
                  </label>
                <Input
                  id="experience"
                  type="text"
                  placeholder="Например: 5 лет"
                  value={formData.experience}
                  onChange={(e) =>
                    setFormData({ ...formData, experience: e.target.value })
                  }
                  className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                  <label htmlFor="motivation" className="block mb-2 text-sm text-gray-700">
                    {getTranslation(membershipTranslations.motivation, language)} {language === "ru" ? "для вступления" : "for joining"} *
                  </label>
                <Textarea
                  id="motivation"
                  placeholder="Расскажите, почему вы хотите стать членом ОСПК..."
                  value={formData.motivation}
                  onChange={(e) =>
                    setFormData({ ...formData, motivation: e.target.value })
                  }
                  className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500 min-h-[120px] resize-none"
                  required
                />
              </div>

              <div className="space-y-4 border-t border-gray-200 pt-6">
                <div className="flex items-start gap-3">
                  <input
                    id="privacyConsent"
                    type="checkbox"
                    checked={formData.privacyConsent}
                    onChange={(e) =>
                      setFormData({ ...formData, privacyConsent: e.target.checked })
                    }
                    className="w-4 h-4 mt-1 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
                    required
                  />
                  <label htmlFor="privacyConsent" className="text-sm text-gray-700 leading-relaxed">
                    Я ознакомлен(а) и согласен(а) с{" "}
                    <span 
                      className="text-blue-600 cursor-pointer hover:underline"
                      onClick={(e) => {
                        e.preventDefault();
                        setModalOpen('privacy');
                      }}
                    >
                      Политикой конфиденциальности
                    </span> *
                  </label>
                </div>

                <div className="flex items-start gap-3">
                  <input
                    id="dataProcessingConsent"
                    type="checkbox"
                    checked={formData.dataProcessingConsent}
                    onChange={(e) =>
                      setFormData({ ...formData, dataProcessingConsent: e.target.checked })
                    }
                    className="w-4 h-4 mt-1 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
                    required
                  />
                  <label htmlFor="dataProcessingConsent" className="text-sm text-gray-700 leading-relaxed">
                    Я даю{" "}
                    <span 
                      className="text-blue-600 cursor-pointer hover:underline"
                      onClick={(e) => {
                        e.preventDefault();
                        setModalOpen('data-processing');
                      }}
                    >
                      согласие на обработку персональных данных
                    </span> *
                  </label>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-6"
              >
                {getTranslation(membershipData.submitButtonText, language)}
              </Button>

              <p className="text-sm text-gray-500 text-center">
                {getTranslation(membershipData.submitMessage, language)}
              </p>
            </form>
          </div>
        </motion.div>
      </div>
      
      {/* Legal Modals */}
      <LegalModal
        isOpen={modalOpen === "privacy"}
        onClose={() => setModalOpen(null)}
        type="privacy"
      />
      <LegalModal
        isOpen={modalOpen === "data-processing"}
        onClose={() => setModalOpen(null)}
        type="data-processing"
      />
    </section>
  );
}