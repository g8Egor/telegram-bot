// Хелпер для динамической загрузки иконок из lucide-react
import * as LucideIcons from "lucide-react";

export type IconName = keyof typeof LucideIcons;

export function getIconComponent(iconName: string): React.ComponentType<any> {
  const Icon = (LucideIcons as any)[iconName];
  if (!Icon) {
    console.warn(`Icon "${iconName}" not found in lucide-react`);
    return LucideIcons.HelpCircle; // Fallback иконка
  }
  return Icon;
}

