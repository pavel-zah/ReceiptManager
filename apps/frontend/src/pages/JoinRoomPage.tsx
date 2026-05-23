import React, { useState } from 'react';
import { colors, spacing, typography } from '@/styles/theme';
import {
  PageContainer,
  PageContent,
  PageFooter,
  Button,
  Input,
  Header,
  ErrorAlert,
  Loading,
} from '@/components/UI';
import { useAppStore } from '@/hooks/useAppStore';
import { roomAPI } from '@/utils/api';
import { hapticFeedback, showTelegramAlert } from '@/utils/telegram';

export const JoinRoomPage: React.FC = () => {
  const { setCurrentPage, setCurrentRoom, setIsLoading, isLoading, error, setError } = useAppStore();
  const [code, setCode] = useState('');
  const [inputError, setInputError] = useState('');

  const handleJoin = async () => {
    if (!code.trim()) {
      setInputError('Пожалуйста, введите код');
      return;
    }

    setIsLoading(true);
    setError(null);
    setInputError('');

    try {
      const room = await roomAPI.findByCode(code.trim());
      setCurrentRoom(room, 'participant');
      hapticFeedback('success');
      setCurrentPage('select-items');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Не удалось присоединиться';
      setError(message);
      setInputError('Неверный код');
      hapticFeedback('impact');
      showTelegramAlert(`Ошибка: ${message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <PageContainer>
      <Header title="Присоединиться" onBack={() => setCurrentPage('home')} />

      <PageContent>
        {isLoading && <Loading fullScreen />}

        {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}

        <div style={{ textAlign: 'center', marginTop: spacing.xl }}>
          <div style={{ fontSize: '48px', marginBottom: spacing.lg }}>🔗</div>
          <p style={{ ...typography.body, color: colors.textSecondary }}>
            Введите код приглашения, которым вас пригласил организатор
          </p>
        </div>

        <div style={{ marginTop: spacing.xl }}>
          <Input
            label="Код комнаты"
            placeholder="например: ABC123"
            value={code}
            onChange={(e) => {
              setCode(e.target.value.toUpperCase());
              setInputError('');
            }}
            error={inputError}
            disabled={isLoading}
            style={{ textAlign: 'center' }}
          />
        </div>
      </PageContent>

      <PageFooter>
        <Button fullWidth size="lg" onClick={handleJoin} loading={isLoading}>
          Присоединиться
        </Button>
      </PageFooter>
    </PageContainer>
  );
};
