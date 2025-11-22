import { Language } from "../contexts/LanguageContext";

/**
 * Хелпер для получения переведенного значения из объекта { ru, en }
 */
export function getTranslation<T extends { ru: string; en: string }>(
  obj: T,
  language: Language
): string {
  return obj[language];
}

/**
 * Хелпер для получения переведенного значения из опционального объекта
 */
export function getOptionalTranslation<T extends { ru: string; en: string }>(
  obj: T | undefined,
  language: Language,
  fallback: string = ""
): string {
  if (!obj) return fallback;
  return obj[language];
}

/**
 * Хелпер для получения переведенного массива строк
 */
export function getTranslatedArray(
  arr: { ru: string; en: string }[],
  language: Language
): string[] {
  return arr.map((item) => item[language]);
}

