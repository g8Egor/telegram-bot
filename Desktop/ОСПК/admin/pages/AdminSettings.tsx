import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "motion/react";
import { ArrowLeft, Save } from "lucide-react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Textarea } from "../../components/ui/textarea";
import { dataStorage } from "../../lib/dataStorage";
import { useLanguage } from "../../contexts/LanguageContext";
import { adminTranslations } from "../../i18n/admin";
import { getTranslation } from "../../utils/i18n";

export function AdminSettings() {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const [activeTab, setActiveTab] = useState<"hero" | "about" | "footer">("hero");
  
  const [hero, setHero] = useState(dataStorage.getHero());
  const [about, setAbout] = useState(dataStorage.getAbout());
  const [footer, setFooter] = useState(dataStorage.getFooter());

  const handleSaveHero = () => {
    dataStorage.saveHero(hero);
    alert(getTranslation(adminTranslations.dataSaved, language));
  };

  const handleSaveAbout = () => {
    dataStorage.saveAbout(about);
    alert(getTranslation(adminTranslations.dataSaved, language));
  };

  const handleSaveFooter = () => {
    dataStorage.saveFooter(footer);
    alert(getTranslation(adminTranslations.dataSaved, language));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={() => navigate("/admin")}
            className="mb-4"
          >
            <ArrowLeft size={18} className="mr-2" />
            {getTranslation(adminTranslations.backToDashboard, language)}
          </Button>
          <h1 className="text-3xl font-bold text-gray-900">{getTranslation(adminTranslations.generalSettings, language)}</h1>
          <p className="text-gray-600 mt-2">{getTranslation(adminTranslations.settingsDescription, language)}</p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-6">
          <div className="flex border-b border-gray-200">
            {[
              { id: "hero" as const, label: adminTranslations.heroPage },
              { id: "about" as const, label: adminTranslations.aboutSection },
              { id: "footer" as const, label: adminTranslations.footer },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-4 font-medium transition-colors ${
                  activeTab === tab.id
                    ? "text-blue-600 border-b-2 border-blue-600"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                {getTranslation(tab.label, language)}
              </button>
            ))}
          </div>

          <div className="p-6">
            {/* Hero Tab */}
            {activeTab === "hero" && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Бейдж (русский)" : "Badge (Russian)"}
                  </label>
                  <Input
                    value={hero.badge.ru}
                    onChange={(e) => setHero({ ...hero, badge: { ...hero.badge, ru: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Бейдж (английский)" : "Badge (English)"}
                  </label>
                  <Input
                    value={hero.badge.en}
                    onChange={(e) => setHero({ ...hero, badge: { ...hero.badge, en: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок (русский)" : "Title (Russian)"}
                  </label>
                  <Input
                    value={hero.title.ru}
                    onChange={(e) => setHero({ ...hero, title: { ...hero.title, ru: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок (английский)" : "Title (English)"}
                  </label>
                  <Input
                    value={hero.title.en}
                    onChange={(e) => setHero({ ...hero, title: { ...hero.title, en: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Описание (русский)" : "Description (Russian)"}
                  </label>
                  <Textarea
                    value={hero.description.ru}
                    onChange={(e) => setHero({ ...hero, description: { ...hero.description, ru: e.target.value } })}
                    rows={3}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Описание (английский)" : "Description (English)"}
                  </label>
                  <Textarea
                    value={hero.description.en}
                    onChange={(e) => setHero({ ...hero, description: { ...hero.description, en: e.target.value } })}
                    rows={3}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Текст кнопки (русский)" : "Button Text (Russian)"}
                  </label>
                  <Input
                    value={hero.buttonText.ru}
                    onChange={(e) => setHero({ ...hero, buttonText: { ...hero.buttonText, ru: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Текст кнопки (английский)" : "Button Text (English)"}
                  </label>
                  <Input
                    value={hero.buttonText.en}
                    onChange={(e) => setHero({ ...hero, buttonText: { ...hero.buttonText, en: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    URL фонового изображения
                  </label>
                  <Input
                    value={hero.backgroundImage}
                    onChange={(e) => setHero({ ...hero, backgroundImage: e.target.value })}
                  />
                </div>
                <Button onClick={handleSaveHero} className="bg-blue-600 hover:bg-blue-700">
                  <Save size={18} className="mr-2" />
                  {getTranslation(adminTranslations.save, language)}
                </Button>
              </div>
            )}

            {/* About Tab */}
            {activeTab === "about" && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок секции (русский)" : "Section Title (Russian)"}
                  </label>
                  <Input
                    value={about.title.ru}
                    onChange={(e) => setAbout({ ...about, title: { ...about.title, ru: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок секции (английский)" : "Section Title (English)"}
                  </label>
                  <Input
                    value={about.title.en}
                    onChange={(e) => setAbout({ ...about, title: { ...about.title, en: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Описание (русский)" : "Description (Russian)"}
                  </label>
                  <Textarea
                    value={about.description.ru}
                    onChange={(e) => setAbout({ ...about, description: { ...about.description, ru: e.target.value } })}
                    rows={2}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Описание (английский)" : "Description (English)"}
                  </label>
                  <Textarea
                    value={about.description.en}
                    onChange={(e) => setAbout({ ...about, description: { ...about.description, en: e.target.value } })}
                    rows={2}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок 'Кто мы' (русский)" : "'Who We Are' Title (Russian)"}
                  </label>
                  <Input
                    value={about.whoWeAre.title.ru}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        whoWeAre: { ...about.whoWeAre, title: { ...about.whoWeAre.title, ru: e.target.value } },
                      })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок 'Кто мы' (английский)" : "'Who We Are' Title (English)"}
                  </label>
                  <Input
                    value={about.whoWeAre.title.en}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        whoWeAre: { ...about.whoWeAre, title: { ...about.whoWeAre.title, en: e.target.value } },
                      })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Параграфы 'Кто мы' (русский, каждый с новой строки)" : "'Who We Are' Paragraphs (Russian, one per line)"}
                  </label>
                  <Textarea
                    value={about.whoWeAre.paragraphs.map(p => p.ru).join("\n")}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        whoWeAre: {
                          ...about.whoWeAre,
                          paragraphs: e.target.value.split("\n").filter((p) => p.trim()).map(text => ({ ru: text, en: "" })),
                        },
                      })
                    }
                    rows={4}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Параграфы 'Кто мы' (английский, каждый с новой строки)" : "'Who We Are' Paragraphs (English, one per line)"}
                  </label>
                  <Textarea
                    value={about.whoWeAre.paragraphs.map(p => p.en).join("\n")}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        whoWeAre: {
                          ...about.whoWeAre,
                          paragraphs: about.whoWeAre.paragraphs.map((p, i) => {
                            const lines = e.target.value.split("\n").filter((p) => p.trim());
                            return { ru: p.ru, en: lines[i] || "" };
                          }),
                        },
                      })
                    }
                    rows={4}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок 'Цели и задачи' (русский)" : "'Goals' Title (Russian)"}
                  </label>
                  <Input
                    value={about.goals.title.ru}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        goals: { ...about.goals, title: { ...about.goals.title, ru: e.target.value } },
                      })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Заголовок 'Цели и задачи' (английский)" : "'Goals' Title (English)"}
                  </label>
                  <Input
                    value={about.goals.title.en}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        goals: { ...about.goals, title: { ...about.goals.title, en: e.target.value } },
                      })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Цели (русский, каждая с новой строки)" : "Goals (Russian, one per line)"}
                  </label>
                  <Textarea
                    value={about.goals.items.map(i => i.ru).join("\n")}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        goals: {
                          ...about.goals,
                          items: e.target.value.split("\n").filter((i) => i.trim()).map(text => ({ ru: text, en: "" })),
                        },
                      })
                    }
                    rows={6}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Цели (английский, каждая с новой строки)" : "Goals (English, one per line)"}
                  </label>
                  <Textarea
                    value={about.goals.items.map(i => i.en).join("\n")}
                    onChange={(e) =>
                      setAbout({
                        ...about,
                        goals: {
                          ...about.goals,
                          items: about.goals.items.map((item, i) => {
                            const lines = e.target.value.split("\n").filter((i) => i.trim());
                            return { ru: item.ru, en: lines[i] || "" };
                          }),
                        },
                      })
                    }
                    rows={6}
                  />
                </div>
                <Button onClick={handleSaveAbout} className="bg-blue-600 hover:bg-blue-700">
                  <Save size={18} className="mr-2" />
                  Сохранить
                </Button>
              </div>
            )}

            {/* Footer Tab */}
            {activeTab === "footer" && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Название организации (русский)" : "Organization Name (Russian)"}
                  </label>
                  <Input
                    value={footer.organizationName.ru}
                    onChange={(e) => setFooter({ ...footer, organizationName: { ...footer.organizationName, ru: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Название организации (английский)" : "Organization Name (English)"}
                  </label>
                  <Input
                    value={footer.organizationName.en}
                    onChange={(e) => setFooter({ ...footer, organizationName: { ...footer.organizationName, en: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Описание (русский)" : "Description (Russian)"}
                  </label>
                  <Textarea
                    value={footer.description.ru}
                    onChange={(e) => setFooter({ ...footer, description: { ...footer.description, ru: e.target.value } })}
                    rows={3}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Описание (английский)" : "Description (English)"}
                  </label>
                  <Textarea
                    value={footer.description.en}
                    onChange={(e) => setFooter({ ...footer, description: { ...footer.description, en: e.target.value } })}
                    rows={3}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <Input
                    value={footer.email}
                    onChange={(e) => setFooter({ ...footer, email: e.target.value })}
                    type="email"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Телефон
                  </label>
                  <Input
                    value={footer.phone}
                    onChange={(e) => setFooter({ ...footer, phone: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Копирайт (русский)" : "Copyright (Russian)"}
                  </label>
                  <Input
                    value={footer.copyright.ru}
                    onChange={(e) => setFooter({ ...footer, copyright: { ...footer.copyright, ru: e.target.value } })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === "ru" ? "Копирайт (английский)" : "Copyright (English)"}
                  </label>
                  <Input
                    value={footer.copyright.en}
                    onChange={(e) => setFooter({ ...footer, copyright: { ...footer.copyright, en: e.target.value } })}
                  />
                </div>
                <Button onClick={handleSaveFooter} className="bg-blue-600 hover:bg-blue-700">
                  <Save size={18} className="mr-2" />
                  Сохранить
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

