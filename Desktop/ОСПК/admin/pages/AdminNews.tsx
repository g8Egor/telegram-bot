import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "motion/react";
import { ArrowLeft, Plus, Edit2, Trash2, Save, X } from "lucide-react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Textarea } from "../../components/ui/textarea";
import { dataStorage } from "../../lib/dataStorage";
import { useLanguage } from "../../contexts/LanguageContext";
import { adminTranslations } from "../../i18n/admin";
import { getTranslation } from "../../utils/i18n";
import type { NewsItem, NewsData } from "../../data/types";

export function AdminNews() {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const [news, setNews] = useState<NewsData>(dataStorage.getNews());
  const [editingId, setEditingId] = useState<string | null>(null);
  const [isAdding, setIsAdding] = useState(false);
  const [formData, setFormData] = useState<NewsItem>({
    id: "",
    title: { ru: "", en: "" },
    date: "",
    excerpt: { ru: "", en: "" },
    image: "",
    content: { ru: "", en: "" },
  });

  const handleEdit = (item: NewsItem) => {
    setFormData(item);
    setEditingId(item.id);
    setIsAdding(false);
  };

  const handleAdd = () => {
    setFormData({
      id: `news-${Date.now()}`,
      title: { ru: "", en: "" },
      date: new Date().toLocaleDateString("ru-RU"),
      excerpt: { ru: "", en: "" },
      image: "",
      content: { ru: "", en: "" },
    });
    setIsAdding(true);
    setEditingId(null);
  };

  const handleSave = () => {
    if (!formData.title.ru || !formData.title.en || !formData.excerpt.ru || !formData.excerpt.en || !formData.content.ru || !formData.content.en) {
      alert(getTranslation(adminTranslations.fillRequiredFields, language));
      return;
    }

    const updatedNews = { ...news };
    
    if (isAdding) {
      updatedNews.items.push(formData);
    } else {
      const index = updatedNews.items.findIndex((item) => item.id === editingId);
      if (index !== -1) {
        updatedNews.items[index] = formData;
      }
    }

    setNews(updatedNews);
    dataStorage.saveNews(updatedNews);
    setEditingId(null);
    setIsAdding(false);
    setFormData({
      id: "",
      title: { ru: "", en: "" },
      date: "",
      excerpt: { ru: "", en: "" },
      image: "",
      content: { ru: "", en: "" },
    });
  };

  const handleDelete = (id: string) => {
    if (confirm(getTranslation(adminTranslations.deleteNews, language))) {
      const updatedNews = {
        ...news,
        items: news.items.filter((item) => item.id !== id),
      };
      setNews(updatedNews);
      dataStorage.saveNews(updatedNews);
    }
  };

  const handleCancel = () => {
    setEditingId(null);
    setIsAdding(false);
    setFormData({
      id: "",
      title: { ru: "", en: "" },
      date: "",
      excerpt: { ru: "", en: "" },
      image: "",
      content: { ru: "", en: "" },
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={() => navigate("/admin")}
            className="mb-4"
          >
            <ArrowLeft size={18} className="mr-2" />
            {getTranslation(adminTranslations.backToDashboard, language)}
          </Button>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{getTranslation(adminTranslations.newsManagement, language)}</h1>
              <p className="text-gray-600 mt-2">{getTranslation(adminTranslations.newsDescription, language)}</p>
            </div>
            <Button onClick={handleAdd} className="bg-blue-600 hover:bg-blue-700">
              <Plus size={18} className="mr-2" />
              {getTranslation(adminTranslations.addNews, language)}
            </Button>
          </div>
        </div>

        {/* Form */}
        {(isAdding || editingId) && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6"
          >
            <h2 className="text-xl font-semibold mb-4">
              {isAdding ? getTranslation(adminTranslations.addNews, language) : getTranslation(adminTranslations.editNews, language)}
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsTitleRu, language)} *
                </label>
                <Input
                  value={formData.title.ru}
                  onChange={(e) => setFormData({ ...formData, title: { ...formData.title, ru: e.target.value } })}
                  placeholder="Заголовок новости (русский)"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsTitleEn, language)} *
                </label>
                <Input
                  value={formData.title.en}
                  onChange={(e) => setFormData({ ...formData, title: { ...formData.title, en: e.target.value } })}
                  placeholder="News title (English)"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsDate, language)} *
                </label>
                <Input
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  placeholder="15 ноября 2025"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsExcerptRu, language)} *
                </label>
                <Textarea
                  value={formData.excerpt.ru}
                  onChange={(e) => setFormData({ ...formData, excerpt: { ...formData.excerpt, ru: e.target.value } })}
                  placeholder="Краткое описание новости (русский)"
                  rows={3}
                  required
                />
                <p className="text-xs text-gray-500 mt-1">{language === "ru" ? "Этот текст отображается в карточке новости на главной странице" : "This text is displayed in the news card on the main page"}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsExcerptEn, language)} *
                </label>
                <Textarea
                  value={formData.excerpt.en}
                  onChange={(e) => setFormData({ ...formData, excerpt: { ...formData.excerpt, en: e.target.value } })}
                  placeholder="Short description (English)"
                  rows={3}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsContentRu, language)} *
                </label>
                <Textarea
                  value={formData.content.ru}
                  onChange={(e) => setFormData({ ...formData, content: { ...formData.content, ru: e.target.value } })}
                  placeholder="Полный текст новости (русский)"
                  rows={8}
                  required
                />
                <p className="text-xs text-gray-500 mt-1">{language === "ru" ? "Этот текст будет показан в попапе при клике на кнопку 'Читать далее'" : "This text will be shown in the popup when clicking 'Read more'"}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsContentEn, language)} *
                </label>
                <Textarea
                  value={formData.content.en}
                  onChange={(e) => setFormData({ ...formData, content: { ...formData.content, en: e.target.value } })}
                  placeholder="Full text (English)"
                  rows={8}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.newsImage, language)}
                </label>
                <Input
                  value={formData.image}
                  onChange={(e) => setFormData({ ...formData, image: e.target.value })}
                  placeholder="https://..."
                />
              </div>
              <div className="flex gap-3">
                <Button onClick={handleSave} className="bg-blue-600 hover:bg-blue-700">
                  <Save size={18} className="mr-2" />
                  {getTranslation(adminTranslations.save, language)}
                </Button>
                <Button variant="outline" onClick={handleCancel}>
                  <X size={18} className="mr-2" />
                  {getTranslation(adminTranslations.cancel, language)}
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {/* List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="divide-y divide-gray-200">
            {news.items.map((item) => (
              <div key={item.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{getTranslation(item.title, language)}</h3>
                    <p className="text-sm text-gray-600 mb-2">{item.date}</p>
                    <p className="text-gray-700">{getTranslation(item.excerpt, language)}</p>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(item)}
                      title={getTranslation(adminTranslations.edit, language)}
                    >
                      <Edit2 size={16} />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(item.id)}
                      className="text-red-600 hover:text-red-700"
                      title={getTranslation(adminTranslations.delete, language)}
                    >
                      <Trash2 size={16} />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

