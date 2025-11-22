import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "motion/react";
import { ArrowLeft, Plus, Edit2, Trash2, Save, X } from "lucide-react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { dataStorage } from "../../lib/dataStorage";
import { useLanguage } from "../../contexts/LanguageContext";
import { adminTranslations } from "../../i18n/admin";
import { getTranslation } from "../../utils/i18n";
import type { TeamMember, TeamData } from "../../data/types";

export function AdminTeam() {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const [team, setTeam] = useState<TeamData>(dataStorage.getTeam());
  const [editingId, setEditingId] = useState<string | null>(null);
  const [isAdding, setIsAdding] = useState(false);
  const [formData, setFormData] = useState<TeamMember>({
    id: "",
    name: { ru: "", en: "" },
    role: { ru: "", en: "" },
    specialty: { ru: "", en: "" },
    initials: "",
    color: "from-blue-500 to-blue-600",
    email: "",
    linkedin: "",
  });

  const handleEdit = (member: TeamMember) => {
    setFormData(member);
    setEditingId(member.id);
    setIsAdding(false);
  };

  const handleAdd = () => {
    const initials = "НМ"; // Можно будет редактировать
    setFormData({
      id: `team-${Date.now()}`,
      name: { ru: "", en: "" },
      role: { ru: "", en: "" },
      specialty: { ru: "", en: "" },
      initials,
      color: "from-blue-500 to-blue-600",
      email: "",
      linkedin: "",
    });
    setIsAdding(true);
    setEditingId(null);
  };

  const handleSave = () => {
    if (!formData.name.ru || !formData.name.en || !formData.role.ru || !formData.role.en || !formData.specialty.ru || !formData.specialty.en) {
      alert(getTranslation(adminTranslations.fillRequiredFields, language));
      return;
    }

    // Автоматически генерируем инициалы из русского имени
    const initials = formData.name.ru
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);

    const memberData = { ...formData, initials };

    const updatedTeam = { ...team };
    
    if (isAdding) {
      updatedTeam.members.push(memberData);
    } else {
      const index = updatedTeam.members.findIndex((m) => m.id === editingId);
      if (index !== -1) {
        updatedTeam.members[index] = memberData;
      }
    }

    setTeam(updatedTeam);
    dataStorage.saveTeam(updatedTeam);
    setEditingId(null);
    setIsAdding(false);
    alert(getTranslation(adminTranslations.dataSaved, language));
    handleCancel();
  };

  const handleDelete = (id: string) => {
    if (confirm(getTranslation(adminTranslations.deleteTeamMember, language))) {
      const updatedTeam = {
        ...team,
        members: team.members.filter((m) => m.id !== id),
      };
      setTeam(updatedTeam);
      dataStorage.saveTeam(updatedTeam);
    }
  };

  const handleCancel = () => {
    setEditingId(null);
    setIsAdding(false);
    setFormData({
      id: "",
      name: { ru: "", en: "" },
      role: { ru: "", en: "" },
      specialty: { ru: "", en: "" },
      initials: "",
      color: "from-blue-500 to-blue-600",
      email: "",
      linkedin: "",
    });
  };

  const colorOptions = [
    { value: "from-blue-500 to-blue-600", label: "Синий" },
    { value: "from-purple-500 to-purple-600", label: "Фиолетовый" },
    { value: "from-teal-500 to-teal-600", label: "Бирюзовый" },
    { value: "from-orange-500 to-orange-600", label: "Оранжевый" },
    { value: "from-pink-500 to-pink-600", label: "Розовый" },
    { value: "from-indigo-500 to-indigo-600", label: "Индиго" },
    { value: "from-cyan-500 to-cyan-600", label: "Циан" },
    { value: "from-emerald-500 to-emerald-600", label: "Изумрудный" },
  ];

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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{getTranslation(adminTranslations.teamManagement, language)}</h1>
              <p className="text-gray-600 mt-2">{getTranslation(adminTranslations.teamDescription, language)}</p>
            </div>
            <Button onClick={handleAdd} className="bg-blue-600 hover:bg-blue-700">
              <Plus size={18} className="mr-2" />
              {getTranslation(adminTranslations.addTeamMember, language)}
            </Button>
          </div>
        </div>

        {(isAdding || editingId) && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6"
          >
            <h2 className="text-xl font-semibold mb-4">
              {isAdding ? getTranslation(adminTranslations.addTeamMember, language) : getTranslation(adminTranslations.editTeamMember, language)}
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.memberNameRu, language)} *
                </label>
                <Input
                  value={formData.name.ru}
                  onChange={(e) => setFormData({ ...formData, name: { ...formData.name, ru: e.target.value } })}
                  placeholder="Иванов Иван Иванович"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.memberNameEn, language)} *
                </label>
                <Input
                  value={formData.name.en}
                  onChange={(e) => setFormData({ ...formData, name: { ...formData.name, en: e.target.value } })}
                  placeholder="Ivan Ivanov"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.memberRoleRu, language)} *
                </label>
                <Input
                  value={formData.role.ru}
                  onChange={(e) => setFormData({ ...formData, role: { ...formData.role, ru: e.target.value } })}
                  placeholder="Председатель сообщества"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.memberRoleEn, language)} *
                </label>
                <Input
                  value={formData.role.en}
                  onChange={(e) => setFormData({ ...formData, role: { ...formData.role, en: e.target.value } })}
                  placeholder="Community Chairman"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.memberSpecialtyRu, language)} *
                </label>
                <Input
                  value={formData.specialty.ru}
                  onChange={(e) => setFormData({ ...formData, specialty: { ...formData.specialty, ru: e.target.value } })}
                  placeholder="Клиническая психология"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {getTranslation(adminTranslations.memberSpecialtyEn, language)} *
                </label>
                <Input
                  value={formData.specialty.en}
                  onChange={(e) => setFormData({ ...formData, specialty: { ...formData.specialty, en: e.target.value } })}
                  placeholder="Clinical Psychology"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Цвет градиента
                </label>
                <select
                  value={formData.color}
                  onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                  className="w-full rounded-md border border-gray-200 px-3 py-2"
                >
                  {colorOptions.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <Input
                  value={formData.email || ""}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  type="email"
                  placeholder="email@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  LinkedIn
                </label>
                <Input
                  value={formData.linkedin || ""}
                  onChange={(e) => setFormData({ ...formData, linkedin: e.target.value })}
                  placeholder="https://linkedin.com/in/..."
                />
              </div>
            </div>
            <div className="flex gap-3 mt-4">
              <Button onClick={handleSave} className="bg-blue-600 hover:bg-blue-700">
                <Save size={18} className="mr-2" />
                {getTranslation(adminTranslations.save, language)}
              </Button>
              <Button variant="outline" onClick={handleCancel}>
                <X size={18} className="mr-2" />
                {getTranslation(adminTranslations.cancel, language)}
              </Button>
            </div>
          </motion.div>
        )}

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="divide-y divide-gray-200">
            {team.members.map((member) => (
              <div key={member.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{getTranslation(member.name, language)}</h3>
                    <p className="text-blue-600 mb-1">{getTranslation(member.role, language)}</p>
                    <p className="text-sm text-gray-600">{getTranslation(member.specialty, language)}</p>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(member)}
                      title={getTranslation(adminTranslations.edit, language)}
                    >
                      <Edit2 size={16} />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(member.id)}
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

