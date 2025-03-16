import { createI18n } from "vue-i18n";

const cacheTrads = {};

async function loadLocaleMessages(locale) {
    if (!cacheTrads[locale]) {
        try {
            const messages = await import(`./${locale}.json`);
            cacheTrads[locale] = messages.default;
        } catch (error) {
            console.error(`Erreur lors du chargement de la langue ${locale}:`, error);
            return;
        }
    }

    i18n.global.setLocaleMessage(locale, cacheTrads[locale]);
    i18n.global.locale.value = locale;
    localStorage.setItem("locale", locale);
}

const i18n = createI18n({
    legacy: false,
    locale: localStorage.getItem("locale") || "fr",
    fallbackLocale: "en",
    messages: {}
});

await loadLocaleMessages(i18n.global.locale.value);

export { i18n, loadLocaleMessages };
