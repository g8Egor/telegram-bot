import { motion } from "motion/react";
import { Send } from "lucide-react";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Textarea } from "./components/ui/textarea";
import { useState } from "react";
import { dataStorage } from "./lib/dataStorage";
import { getIconComponent } from "./utils/iconLoader";
import { useLanguage } from "./contexts/LanguageContext";
import { getTranslation } from "./utils/i18n";

export function ContactsSection() {
  const { language } = useLanguage();
  const contactsData = dataStorage.getContacts();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    // Handle form submission
  };

  return (
    <section className="py-32 px-6 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl mb-6 tracking-tight">
            {getTranslation(contactsData.title, language)}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {getTranslation(contactsData.description, language)}
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* Contact Information */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div>
              <h3 className="text-3xl mb-6 tracking-tight">
                {getTranslation(contactsData.contactTitle, language)}
              </h3>
              <p className="text-lg text-gray-600 mb-8">
                {getTranslation(contactsData.contactDescription, language)}
              </p>
            </div>

            <div className="space-y-6">
              {contactsData.contactInfo.map((item, index) => {
                const IconComponent = getIconComponent(item.icon);
                return (
                <motion.div
                    key={item.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="flex items-start gap-4"
                >
                  <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
                      <IconComponent className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-500 mb-1">{getTranslation(item.label, language)}</div>
                    {item.href ? (
                      <a
                        href={item.href}
                        className="text-lg text-gray-900 hover:text-blue-600 transition-colors"
                      >
                        {item.value}
                      </a>
                    ) : (
                      <div className="text-lg text-gray-900">{item.value}</div>
                    )}
                  </div>
                </motion.div>
                );
              })}
            </div>
          </motion.div>

          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="bg-white rounded-3xl p-8 shadow-sm border border-gray-100"
          >
            <h3 className="text-2xl mb-6 tracking-tight">
              {getTranslation(contactsData.formTitle, language)}
            </h3>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block mb-2 text-sm text-gray-700">
                  {getTranslation(contactsData.formNameLabel, language)}
                </label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Иван Иванов"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="email" className="block mb-2 text-sm text-gray-700">
                  {getTranslation(contactsData.formEmailLabel, language)}
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="ivan@example.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="message" className="block mb-2 text-sm text-gray-700">
                  {getTranslation(contactsData.formMessageLabel, language)}
                </label>
                <Textarea
                  id="message"
                  placeholder="Расскажите, чем мы можем вам помочь..."
                  value={formData.message}
                  onChange={(e) =>
                    setFormData({ ...formData, message: e.target.value })
                  }
                  className="w-full rounded-xl border-gray-200 focus:border-blue-500 focus:ring-blue-500 min-h-[150px] resize-none"
                  required
                />
              </div>

              <Button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-6 gap-2"
              >
                <Send size={18} />
                {getTranslation(contactsData.formSubmitText, language)}
              </Button>
            </form>

            <p className="text-sm text-gray-500 mt-6 text-center">
              {getTranslation(contactsData.formResponseTime, language)}
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}