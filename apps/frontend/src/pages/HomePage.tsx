import React, { useEffect } from 'react';
import { colors, spacing, typography, borderRadius } from '@/styles/theme';
import {
  PageContainer,
  PageContent,
  PageFooter,
  Button,
} from '@/components/UI';
import { useAppStore } from '@/hooks/useAppStore';

const steps = [
  { emoji: '📸', title: 'Фото чека',    desc: 'Сфотографируйте чек или загрузите из галереи', bg: colors.pastelPeach },
  { emoji: '👥', title: 'Друзья',       desc: 'Пригласите участников по ссылке или коду',      bg: colors.pastelCoral },
  { emoji: '✅', title: 'Выбор',        desc: 'Каждый отмечает свои позиции',                  bg: colors.pastelYellow },
  { emoji: '💸', title: 'Итог',         desc: 'Все видят свою сумму мгновенно',                bg: colors.pastelPink },
];

export const HomePage: React.FC = () => {
  const { setCurrentPage } = useAppStore();

  useEffect(() => {
    window.Telegram?.WebApp?.expand();
  }, []);

  return (
    <PageContainer>
      <PageContent>
        {/* Hero */}
        <div style={{ textAlign: 'center', paddingTop: spacing.xl, paddingBottom: spacing.lg }}>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '80px',
              height: '80px',
              borderRadius: '28px',
              backgroundColor: colors.pastelPeach,
              fontSize: '40px',
              marginBottom: spacing.lg,
              boxShadow: `0 4px 20px ${colors.shadow}`,
            }}
          >
            🧾
          </div>
          <h1
            style={{
              ...typography.title,
              fontSize: '26px',
              fontWeight: 700,
              color: colors.text,
              marginBottom: spacing.sm,
            }}
          >
            Receipt Manager
          </h1>
          <p style={{ ...typography.body, color: colors.textSecondary }}>
            Умный способ разделить счёт с друзьями
          </p>
        </div>

        {/* Bento: Как это работает? */}
        <div style={{ marginBottom: spacing.lg }}>
          <p
            style={{
              ...typography.bodySmall,
              fontWeight: 600,
              color: colors.textSecondary,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              marginBottom: spacing.md,
            }}
          >
            Как это работает?
          </p>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: spacing.md,
            }}
          >
            {steps.map((step, i) => (
              <div
                key={i}
                style={{
                  backgroundColor: step.bg,
                  borderRadius: borderRadius.lg,
                  padding: spacing.lg,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: spacing.sm,
                  minHeight: '120px',
                }}
              >
                <div style={{ fontSize: '28px' }}>{step.emoji}</div>
                <div style={{ ...typography.subtitle, color: colors.text, fontWeight: 600 }}>
                  {step.title}
                </div>
                <div style={{ ...typography.bodySmall, color: colors.textSecondary, lineHeight: '1.4' }}>
                  {step.desc}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bento: stats / tagline */}
        <div
          style={{
            backgroundColor: colors.pastelCoral,
            borderRadius: borderRadius.lg,
            padding: spacing.lg,
            display: 'flex',
            justifyContent: 'space-around',
            alignItems: 'center',
            gap: spacing.md,
          }}
        >
          {[
            { val: 'AI', label: 'Распознавание' },
            { val: '⚡', label: 'Мгновенно' },
            { val: '∞', label: 'Участников' },
          ].map(({ val, label }) => (
            <div key={label} style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '22px', fontWeight: 700, color: colors.text }}>{val}</div>
              <div style={{ ...typography.bodySmall, color: colors.textSecondary }}>{label}</div>
            </div>
          ))}
        </div>
      </PageContent>

      <PageFooter>
        <div style={{ display: 'flex', flexDirection: 'column', gap: spacing.md }}>
          <Button
            fullWidth
            size="lg"
            onClick={() => setCurrentPage('create-room')}
          >
            ➕ Создать комнату
          </Button>
          <Button
            fullWidth
            size="lg"
            variant="secondary"
            onClick={() => setCurrentPage('room-code')}
          >
            🔗 Присоединиться
          </Button>
        </div>
      </PageFooter>
    </PageContainer>
  );
};
