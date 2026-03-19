import React, { useState } from 'react';
import {
  PageContainer,
  PageContent,
  PageFooter,
  Button,
  Header,
  Loading,
  ErrorAlert,
} from '@/components/UI';
import { ReceiptItemList, ReceiptSummary } from '@/components/ReceiptItems';
import { useAppStore } from '@/hooks/useAppStore';
import { roomAPI } from '@/utils/api';
import { hapticFeedback, showTelegramAlert } from '@/utils/telegram';
import { spacing } from '@/styles/theme';

export const SelectItemsPage: React.FC = () => {
  const {
    currentRoom,
    setCurrentPage,
    selectedItems,
    updateItemSelection,
    clearSelection,
    setError: setAppError,
    error,
    setError,
  } = useAppStore();
  const [isLoading, setIsLoading] = useState(false);

  if (!currentRoom?.receipt) {
    return (
      <PageContainer>
        <PageContent>
          <Loading fullScreen />
        </PageContent>
      </PageContainer>
    );
  }

  const receipt = currentRoom.receipt;
  const handleSubmitSelection = async () => {
    if (Object.keys(selectedItems).length === 0) {
      showTelegramAlert('Пожалуйста, выберите хотя бы одну позицию');
      hapticFeedback('impact');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Update selections in backend
      for (const [itemId, quantity] of Object.entries(selectedItems)) {
        await roomAPI.assignItemToUser(currentRoom.id, itemId, currentRoom.creatorId, quantity);
      }

      hapticFeedback('success');
      setCurrentPage('results');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при отправке выбора';
      setAppError(message);
      hapticFeedback('impact');
      showTelegramAlert(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <PageContainer>
      <Header
        title="Выберите свое"
        onBack={() => {
          clearSelection();
          setCurrentPage('home');
        }}
      />

      <PageContent>
        {isLoading && <Loading />}

        {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}

        <ReceiptItemList
          items={receipt.items}
          selectedItems={selectedItems}
          onSelectItem={updateItemSelection}
          mode="select"
        />

        <ReceiptSummary
          items={receipt.items}
          selectedItems={selectedItems}
          tip={receipt.tip}
          service={receipt.service}
        />
      </PageContent>

      <PageFooter>
        <div style={{ display: 'flex', gap: spacing.md }}>
          <Button
            fullWidth
            variant="secondary"
            onClick={() => {
              clearSelection();
              setCurrentPage('home');
            }}
            disabled={isLoading}
          >
            Отмена
          </Button>
          <Button fullWidth onClick={handleSubmitSelection} loading={isLoading}>
            Готово
          </Button>
        </div>
      </PageFooter>
    </PageContainer>
  );
};
