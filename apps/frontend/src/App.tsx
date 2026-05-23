import React, { useEffect } from 'react';
import { colors } from '@/styles/theme';
import { useAppStore } from '@/hooks/useAppStore';
import { initTelegramApp, getTelegramUser } from '@/utils/telegram';
import { HomePage } from '@/pages/HomePage';
import { JoinRoomPage } from '@/pages/JoinRoomPage';
import { SelectItemsPage } from '@/pages/SelectItemsPage';
import { ResultsPage } from '@/pages/ResultsPage';
import { CreateRoomPage } from '@/pages/CreateRoomPage';
import { RoomPage } from '@/pages/RoomPage';

export const APP: React.FC = () => {
  const { currentPage, setTelegramUser } = useAppStore();

  useEffect(() => {
    // Initialize Telegram Web App
    const tgApp = initTelegramApp();
    if (tgApp) {
      tgApp.setBackgroundColor('FFFAF6');
      tgApp.setHeaderColor('FFFAF6');

      const user = getTelegramUser();
      if (user) {
        setTelegramUser(user);
      }
    }

    // Inject global styles
    const style = document.createElement('style');
    style.textContent = `
      @keyframes spin {
        to { transform: rotate(360deg); }
      }

      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      html, body, #root {
        width: 100%;
        height: 100%;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      body {
        background-color: #FFFAF6;
        color: #2D1F14;
      }

      button, input, textarea, select {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
      }

      button {
        border: none;
        outline: none;
      }

      button:focus, button:focus-visible {
        outline: none;
        box-shadow: none;
      }

      input:focus, textarea:focus {
        outline: none;
      }

      ::placeholder {
        color: #99a2ad;
      }

      ::-webkit-scrollbar {
        width: 6px;
      }

      ::-webkit-scrollbar-track {
        background: transparent;
      }

      ::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 3px;
      }
    `;
    document.head.appendChild(style);
  }, [setTelegramUser]);

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage />;
      case 'create-room':
        return <CreateRoomPage />;
      case 'room-code':
        return <JoinRoomPage />;
      case 'select-items':
        return <SelectItemsPage />;
      case 'results':
        return <ResultsPage />;
      case 'room':
        return <RoomPage />;
      default:
        return <HomePage />;
    }
  };

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        backgroundColor: colors.background,
      }}
    >
      {renderPage()}
    </div>
  );
};

export default APP;
