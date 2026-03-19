import React, { useState, useRef } from 'react';
import { colors, spacing, typography, borderRadius } from '@/styles/theme';
import {
  PageContainer,
  PageContent,
  PageFooter,
  Button,
  Input,
  Header,
  Card,
  ErrorAlert,
  Loading,
} from '@/components/UI';
import { ReceiptItemList, ReceiptSummary } from '@/components/ReceiptItems';
import { useAppStore } from '@/hooks/useAppStore';
import { receiptAPI } from '@/utils/api';
import { hapticFeedback, showTelegramAlert } from '@/utils/telegram';
import type { Receipt } from '@/types';

type CreateRoomStep = 'upload' | 'review' | 'adjust' | 'share';

export const CreateRoomPage: React.FC = () => {
  const { setCurrentPage, setCurrentRoom } = useAppStore();
  const [step, setStep] = useState<CreateRoomStep>('upload');
  const [receipt, setReceipt] = useState<Receipt | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newItemName, setNewItemName] = useState('');
  const [newItemPrice, setNewItemPrice] = useState('');
  const [newItemQty, setNewItemQty] = useState('1');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);

    // --- MOCK: skip API, use fake receipt data ---
    await new Promise((r) => setTimeout(r, 800)); // simulate loading

    const mockReceipt: Receipt = {
      id: 'mock-' + Math.random().toString(36).slice(2, 8),
      paidAt: new Date().toISOString(),
      tip: 0,
      service: 0,
      totalSum: 1850,
      items: [
        { id: 'item-1', name: 'Паста Карбонара',     price: 550,  quantity: 1, assignedUsers: [] },
        { id: 'item-2', name: 'Пицца Маргарита',     price: 720,  quantity: 1, assignedUsers: [] },
        { id: 'item-3', name: 'Лимонад',             price: 180,  quantity: 2, assignedUsers: [] },
        { id: 'item-4', name: 'Тирамису',            price: 220,  quantity: 1, assignedUsers: [] },
      ],
    };

    setReceipt(mockReceipt);
    setStep('review');
    hapticFeedback('success');
    setIsLoading(false);
  };

  const handleAddItem = async () => {
    if (!receipt || !newItemName.trim() || !newItemPrice.trim()) {
      setError('Заполните все поля');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const price = parseFloat(newItemPrice);
      const qty = parseInt(newItemQty) || 1;
      const updated = await receiptAPI.addItem(receipt.id, newItemName, price, qty);
      setReceipt(updated);
      setNewItemName('');
      setNewItemPrice('');
      setNewItemQty('1');
      hapticFeedback('success');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при добавлении позиции';
      setError(message);
      hapticFeedback('impact');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteItem = async (itemId: string) => {
    if (!receipt) return;

    setIsLoading(true);
    setError(null);

    try {
      const updated = await receiptAPI.removeItem(receipt.id, itemId);
      setReceipt(updated);
      hapticFeedback('success');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при удалении позиции';
      setError(message);
      hapticFeedback('impact');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateRoom = async () => {
    if (!receipt) return;

    setIsLoading(true);
    setError(null);

    try {
      // --- MOCK: skip API, create fake room ---
      await new Promise((r) => setTimeout(r, 500));

      const mockRoom = {
        id: 'room-' + Math.random().toString(36).slice(2, 8),
        shareCode: Math.random().toString(36).slice(2, 8).toUpperCase(),
        creatorId: 'user-local',
        receipt,
        receiptId: receipt.id,
        isActive: true,
        participants: [],
        createdAt: new Date().toISOString(),
      };

      setCurrentRoom(mockRoom, 'creator');
      setStep('share');
      hapticFeedback('success');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка при создании комнаты';
      setError(message);
      hapticFeedback('impact');
      showTelegramAlert(message);
    } finally {
      setIsLoading(false);
    }
  };

  if (step === 'upload') {
    return (
      <PageContainer>
        <Header title="Создать комнату" onBack={() => setCurrentPage('home')} />

        <PageContent>
          {isLoading && <Loading fullScreen />}

          {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}

          <div style={{ textAlign: 'center', marginTop: spacing.xl }}>
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '80px',
                height: '80px',
                borderRadius: '28px',
                backgroundColor: colors.pastelBlue,
                fontSize: '40px',
                marginBottom: spacing.lg,
              }}
            >
              📸
            </div>
            <h2 style={{ ...typography.heading, marginBottom: spacing.sm }}>Загрузите фото чека</h2>
            <p style={{ ...typography.body, color: colors.textSecondary }}>
              AI распознает позиции и цены
            </p>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
          />

          <div
            onClick={() => fileInputRef.current?.click()}
            style={{
              textAlign: 'center',
              cursor: 'pointer',
              padding: `${spacing.xl}px ${spacing.lg}px`,
              border: `2px dashed ${colors.primary}`,
              backgroundColor: colors.pastelBlue,
              borderRadius: borderRadius.lg,
              transition: 'opacity 0.2s ease',
            }}
          >
            <div style={{ fontSize: '36px', marginBottom: spacing.sm }}>+</div>
            <p style={{ ...typography.body, color: colors.primary, fontWeight: 500 }}>
              Нажмите, чтобы выбрать файл
            </p>
            <p style={{ ...typography.bodySmall, color: colors.textSecondary, marginTop: 4 }}>
              JPG, PNG, HEIC
            </p>
          </div>
        </PageContent>

        <PageFooter>
          <Button fullWidth size="lg" variant="secondary" onClick={() => setCurrentPage('home')}>
            Отмена
          </Button>
        </PageFooter>
      </PageContainer>
    );
  }

  if (step === 'review' && receipt) {
    return (
      <PageContainer>
        <Header title="Проверьте чек" onBack={() => setStep('upload')} />

        <PageContent>
          {isLoading && <Loading />}

          {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}

          <Card>
            <div style={{ ...typography.subtitle, marginBottom: spacing.md }}>📝 Позиции</div>
            <ReceiptItemList items={receipt.items} mode="edit" onDeleteItem={handleDeleteItem} />
          </Card>

          <Card>
            <div style={{ ...typography.subtitle, marginBottom: spacing.md }}>➕ Добавить позицию</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: spacing.sm }}>
              <Input
                label="Название"
                placeholder="например: Паста"
                value={newItemName}
                onChange={(e) => setNewItemName(e.target.value)}
              />
              <Input
                label="Цена (₽)"
                type="number"
                placeholder="0.00"
                value={newItemPrice}
                onChange={(e) => setNewItemPrice(e.target.value)}
              />
              <Input
                label="Количество"
                type="number"
                value={newItemQty}
                onChange={(e) => setNewItemQty(e.target.value)}
              />
              <Button onClick={handleAddItem} loading={isLoading} fullWidth>
                Добавить
              </Button>
            </div>
          </Card>

          <ReceiptSummary items={receipt.items} tip={receipt.tip} service={receipt.service} />
        </PageContent>

        <PageFooter>
          <Button
            fullWidth
            size="lg"
            onClick={handleCreateRoom}
            loading={isLoading}
          >
            Создать комнату
          </Button>
        </PageFooter>
      </PageContainer>
    );
  }

  if (step === 'share') {
    return (
      <PageContainer>
        <Header title="Комната создана!" />

        <PageContent>
          <div style={{ textAlign: 'center', marginTop: spacing.xl }}>
            <div style={{ fontSize: '60px', marginBottom: spacing.lg }}>✅</div>
            <h2 style={{ ...typography.heading, marginBottom: spacing.md }}>
              Пригласите друзей!
            </h2>
            <p style={{ ...typography.body, color: colors.textSecondary, marginBottom: spacing.xl }}>
              Поделитесь кодом или ссылкой
            </p>
          </div>

          <Card elevated>
            <div style={{ ...typography.subtitle, marginBottom: spacing.md }}>🔑 Код</div>
            <div
              style={{
                backgroundColor: colors.secondaryBg,
                padding: spacing.lg,
                borderRadius: 8,
                textAlign: 'center',
                fontSize: '28px',
                fontWeight: 'bold',
                fontFamily: 'monospace',
              }}
            >
              {receipt?.id.slice(0, 6).toUpperCase()}
            </div>
          </Card>

          <Card>
            <div style={{ ...typography.subtitle, marginBottom: spacing.md }}>📊 Чек</div>
            <ReceiptSummary items={receipt?.items || []} />
          </Card>
        </PageContent>

        <PageFooter>
          <Button
            fullWidth
            size="lg"
            onClick={() => setCurrentPage('room')}
          >
            🚀 Открыть комнату
          </Button>
          <Button
            fullWidth
            size="lg"
            variant="secondary"
            onClick={() => setCurrentPage('home')}
          >
            ← Назад на главную
          </Button>
        </PageFooter>
      </PageContainer>
    );
  }

  return null;
};
