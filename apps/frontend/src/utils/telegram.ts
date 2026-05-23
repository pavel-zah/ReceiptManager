// Telegram Web App integration
declare global {
  interface Window {
    Telegram: {
      WebApp: {
        ready: () => void;
        expand: () => void;
        close: () => void;
        onEvent: (eventType: string, callback: () => void) => void;
        offEvent: (eventType: string, callback?: () => void) => void;
        initData: string;
        initDataUnsafe: {
          user?: {
            id: number;
            is_bot: boolean;
            first_name: string;
            last_name?: string;
            username?: string;
            language_code?: string;
          };
          auth_date: number;
          hash: string;
        };
        platform: string;
        colorScheme: 'light' | 'dark';
        themeParams: {
          bg_color: string;
          secondary_bg_color: string;
          text_color: string;
          hint_color: string;
          link_color: string;
          button_color: string;
          button_text_color: string;
        };
        isExpanded: boolean;
        viewportHeight: number;
        headerColor: string;
        backgroundColor: string;
        setHeaderColor: (color: string) => void;
        setBackgroundColor: (color: string) => void;
        showAlert: (message: string) => void;
        showConfirm: (message: string, callback: (ok: boolean) => void) => void;
        HapticFeedback: {
          impactOccurred: (style: string) => void;
          notificationOccurred: (type: string) => void;
          selectionChanged: () => void;
        };
      };
    };
  }
}

export const initTelegramApp = () => {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.ready();
    window.Telegram.WebApp.expand();
    return window.Telegram.WebApp;
  }
  return null;
};

export const getTelegramUser = () => {
  if (window.Telegram?.WebApp?.initDataUnsafe) {
    return window.Telegram.WebApp.initDataUnsafe.user;
  }
  return null;
};

export const getTelegramInitData = () => {
  return window.Telegram?.WebApp?.initData || '';
};

export const showTelegramAlert = (message: string) => {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.showAlert(message);
  }
};

export const showTelegramConfirm = (message: string): Promise<boolean> => {
  return new Promise((resolve) => {
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.showConfirm(message, (ok) => {
        resolve(ok);
      });
    } else {
      resolve(confirm(message));
    }
  });
};

export const hapticFeedback = (type: 'success' | 'impact' | 'selection' = 'selection') => {
  const haptic = window.Telegram?.WebApp?.HapticFeedback;
  if (!haptic) return;

  switch (type) {
    case 'success':
      haptic.notificationOccurred('success');
      break;
    case 'impact':
      haptic.impactOccurred('medium');
      break;
    case 'selection':
      haptic.selectionChanged();
      break;
  }
};

export const getThemeColor = (key: keyof typeof window.Telegram.WebApp.themeParams): string => {
  return window.Telegram?.WebApp?.themeParams?.[key] || '#ffffff';
};
