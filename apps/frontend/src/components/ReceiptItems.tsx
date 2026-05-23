import React from 'react';
import { colors, spacing, typography, borderRadius } from '@/styles/theme';
import type { ReceiptItem } from '@/types';

interface ReceiptItemListProps {
  items: ReceiptItem[];
  selectedItems?: Record<string, number>;
  onSelectItem?: (itemId: string, quantity: number) => void;
  mode?: 'view' | 'select' | 'edit';
  onEditItem?: (item: ReceiptItem) => void;
  onDeleteItem?: (itemId: string) => void;
}

const ReceiptItemRow: React.FC<{
  item: ReceiptItem;
  selected?: number;
  onSelect?: (quantity: number) => void;
  mode?: 'view' | 'select' | 'edit';
  onEdit?: () => void;
  onDelete?: () => void;
}> = ({ item, selected = 0, onSelect, mode = 'view', onEdit, onDelete }) => {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: `${spacing.md}px ${spacing.md}px`,
        backgroundColor: colors.background,
        borderRadius: borderRadius.sm,
        border: `1px solid ${colors.divider}`,
        marginBottom: spacing.sm,
      }}
    >
      <div style={{ flex: 1 }}>
        <div style={{ ...typography.body, fontWeight: 500 }}>{item.name}</div>
        <div style={{ ...typography.caption, marginTop: spacing.xs }}>
          {item.quantity} шт. × {item.price.toFixed(2)} ₽
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: spacing.md }}>
        <div style={{ ...typography.subtitle, fontWeight: 600 }}>
          {(item.price * item.quantity).toFixed(2)} ₽
        </div>

        {mode === 'select' && onSelect && (
          <div style={{ display: 'flex', alignItems: 'center', gap: spacing.sm }}>
            <button
              onClick={() => onSelect(Math.max(0, selected - 1))}
              style={{
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                backgroundColor: colors.secondaryBg,
                border: 'none',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              −
            </button>
            <span style={{ width: '20px', textAlign: 'center', fontWeight: 600 }}>
              {selected}
            </span>
            <button
              onClick={() => onSelect(Math.min(item.quantity, selected + 1))}
              style={{
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                backgroundColor: colors.primary,
                color: 'white',
                border: 'none',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              +
            </button>
          </div>
        )}

        {mode === 'edit' && (onEdit || onDelete) && (
          <div style={{ display: 'flex', gap: spacing.sm }}>
            {onEdit && (
              <button
                onClick={onEdit}
                style={{
                  background: 'none',
                  color: colors.primary,
                  fontSize: '18px',
                  cursor: 'pointer',
                }}
              >
                ✎
              </button>
            )}
            {onDelete && (
              <button
                onClick={onDelete}
                style={{
                  background: 'none',
                  color: colors.error,
                  fontSize: '18px',
                  cursor: 'pointer',
                }}
              >
                🗑
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export const ReceiptItemList: React.FC<ReceiptItemListProps> = ({
  items,
  selectedItems = {},
  onSelectItem,
  mode = 'view',
  onEditItem,
  onDeleteItem,
}) => {
  return (
    <div>
      {items.length === 0 ? (
        <div
          style={{
            padding: spacing.lg,
            backgroundColor: colors.secondaryBg,
            borderRadius: borderRadius.md,
            textAlign: 'center',
            color: colors.textSecondary,
          }}
        >
          Позиций в чеке нет
        </div>
      ) : (
        items.map((item) => (
          <ReceiptItemRow
            key={item.id}
            item={item}
            selected={selectedItems[item.id] || 0}
            onSelect={(qty) => onSelectItem?.(item.id, qty)}
            mode={mode}
            onEdit={() => onEditItem?.(item)}
            onDelete={() => onDeleteItem?.(item.id)}
          />
        ))
      )}
    </div>
  );
};

interface ReceiptSummaryProps {
  items: ReceiptItem[];
  selectedItems?: Record<string, number>;
  tip?: number;
  service?: number;
}

export const ReceiptSummary: React.FC<ReceiptSummaryProps> = ({
  items,
  selectedItems = {},
  tip = 0,
  service = 0,
}) => {
  const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const total = subtotal + tip + service;
  const selectedTotal = items.reduce((sum, item) => {
    if (selectedItems[item.id]) {
      return sum + (item.price * selectedItems[item.id]);
    }
    return sum;
  }, 0);

  return (
    <div
      style={{
        backgroundColor: colors.background,
        borderRadius: borderRadius.md,
        padding: spacing.lg,
        border: `1px solid ${colors.divider}`,
      }}
    >
      <div style={{ marginBottom: spacing.md }}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            ...typography.body,
            marginBottom: spacing.sm,
          }}
        >
          <span>Позиции:</span>
          <span>{subtotal.toFixed(2)} ₽</span>
        </div>
        {service > 0 && (
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              ...typography.body,
              marginBottom: spacing.sm,
            }}
          >
            <span>Обслуживание:</span>
            <span>{service.toFixed(2)} ₽</span>
          </div>
        )}
        {tip > 0 && (
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              ...typography.body,
              marginBottom: spacing.sm,
            }}
          >
            <span>Чаевые:</span>
            <span>{tip.toFixed(2)} ₽</span>
          </div>
        )}
      </div>
      <div
        style={{
          borderTop: `1px solid ${colors.divider}`,
          paddingTop: spacing.md,
          display: 'flex',
          justifyContent: 'space-between',
          ...typography.subtitle,
          fontWeight: 600,
        }}
      >
        <span>ИТОГО:</span>
        <span>{total.toFixed(2)} ₽</span>
      </div>
      {selectedItems && Object.keys(selectedItems).length > 0 && (
        <div
          style={{
            marginTop: spacing.md,
            paddingTop: spacing.md,
            borderTop: `1px solid ${colors.divider}`,
            display: 'flex',
            justifyContent: 'space-between',
            ...typography.body,
            backgroundColor: colors.secondaryBg,
            padding: spacing.md,
            borderRadius: borderRadius.sm,
          }}
        >
          <span>Ваше:</span>
          <span style={{ fontWeight: 600 }}>{selectedTotal.toFixed(2)} ₽</span>
        </div>
      )}
    </div>
  );
};
