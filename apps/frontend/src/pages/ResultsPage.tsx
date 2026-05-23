import React from 'react';
import { colors, spacing, typography, borderRadius } from '@/styles/theme';
import {
  PageContainer,
  PageContent,
  PageFooter,
  Button,
  Header,
  Card,
} from '@/components/UI';
import { useAppStore } from '@/hooks/useAppStore';

export const ResultsPage: React.FC = () => {
  const { currentRoom, paymentSplits, setCurrentPage, clearCurrentRoom, clearSelection } =
    useAppStore();

  if (!currentRoom) {
    return (
      <PageContainer>
        <PageContent>
          <div>Нет данных</div>
        </PageContent>
      </PageContainer>
    );
  }

  const handleNewRoom = () => {
    clearCurrentRoom();
    clearSelection();
    setCurrentPage('home');
  };

  return (
    <PageContainer>
      <Header title="Расчет" />

      <PageContent>
        <Card elevated>
          <div style={{ ...typography.subtitle, marginBottom: spacing.md }}>💰 Кто сколько платит</div>

          {paymentSplits && paymentSplits.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: spacing.md }}>
              {paymentSplits.map((split, idx) => (
                <div
                  key={idx}
                  style={{
                    backgroundColor: colors.secondaryBg,
                    padding: spacing.md,
                    borderRadius: borderRadius.sm,
                    borderLeft: `4px solid ${colors.primary}`,
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: spacing.sm,
                    }}
                  >
                    <span style={{ ...typography.body, fontWeight: 500 }}>
                      {split.username || `Участник ${idx + 1}`}
                    </span>
                    <span
                      style={{
                        ...typography.heading,
                        color: colors.primary,
                        fontWeight: 600,
                      }}
                    >
                      {split.total.toFixed(2)} ₽
                    </span>
                  </div>

                  {split.items.length > 0 && (
                    <div style={{ ...typography.caption, color: colors.textSecondary }}>
                      {split.items.map((item, i) => (
                        <div key={i}>
                          {item.name} ({item.quantity}x) = {item.subtotal.toFixed(2)} ₽
                        </div>
                      ))}
                    </div>
                  )}

                  {(split.taxShare > 0 || split.tipShare > 0) && (
                    <div
                      style={{
                        ...typography.caption,
                        color: colors.textSecondary,
                        marginTop: spacing.sm,
                        borderTop: `1px solid ${colors.divider}`,
                        paddingTop: spacing.sm,
                      }}
                    >
                      {split.taxShare > 0 && (
                        <div>Налоги: {split.taxShare.toFixed(2)} ₽</div>
                      )}
                      {split.tipShare > 0 && (
                        <div>Чаевые: {split.tipShare.toFixed(2)} ₽</div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div style={{ ...typography.body, color: colors.textSecondary }}>
              Нет данных по участникам
            </div>
          )}
        </Card>

        <Card>
          <div style={{ ...typography.subtitle, marginBottom: spacing.md }}>📋 Информация о чеке</div>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: spacing.sm,
              ...typography.body,
            }}
          >
            <span>Позиций:</span>
            <span>{currentRoom.receipt?.items.length || 0}</span>
          </div>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: spacing.sm,
              ...typography.body,
            }}
          >
            <span>Участников:</span>
            <span>{currentRoom.participants.length}</span>
          </div>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              ...typography.body,
              fontWeight: 600,
            }}
          >
            <span>Всего в чеке:</span>
            <span>{currentRoom.receipt?.totalSum.toFixed(2) || '0'} ₽</span>
          </div>
        </Card>
      </PageContent>

      <PageFooter>
        <Button fullWidth size="lg" onClick={handleNewRoom}>
          ← Начать заново
        </Button>
      </PageFooter>
    </PageContainer>
  );
};
