import { create } from 'zustand';
import type { Room, Receipt, TelegramUser, RoomRole, PaymentSplit } from '@/types';

interface AppState {
  // User
  telegramUser: TelegramUser | null;
  setTelegramUser: (user: TelegramUser) => void;

  // Navigation
  currentPage: string;
  setCurrentPage: (page: string) => void;

  // Room
  currentRoom: Room | null;
  currentRoomRole: RoomRole | null;
  setCurrentRoom: (room: Room, role: RoomRole) => void;
  clearCurrentRoom: () => void;

  // Receipt
  currentReceipt: Receipt | null;
  setCurrentReceipt: (receipt: Receipt) => void;
  clearCurrentReceipt: () => void;

  // Selection
  selectedItems: Record<string, number>; // itemId: quantity
  updateItemSelection: (itemId: string, quantity: number) => void;
  clearSelection: () => void;

  // UI
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;

  // Results
  paymentSplits: PaymentSplit[] | null;
  setPaymentSplits: (splits: PaymentSplit[]) => void;
  clearPaymentSplits: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // User
  telegramUser: null,
  setTelegramUser: (user) => set({ telegramUser: user }),

  // Navigation
  currentPage: 'home',
  setCurrentPage: (page) => set({ currentPage: page }),

  // Room
  currentRoom: null,
  currentRoomRole: null,
  setCurrentRoom: (room, role) => set({ currentRoom: room, currentRoomRole: role }),
  clearCurrentRoom: () => set({ currentRoom: null, currentRoomRole: null }),

  // Receipt
  currentReceipt: null,
  setCurrentReceipt: (receipt) => set({ currentReceipt: receipt }),
  clearCurrentReceipt: () => set({ currentReceipt: null }),

  // Selection
  selectedItems: {},
  updateItemSelection: (itemId, quantity) =>
    set((state) => {
      const newSelection = { ...state.selectedItems };
      if (quantity > 0) {
        newSelection[itemId] = quantity;
      } else {
        delete newSelection[itemId];
      }
      return { selectedItems: newSelection };
    }),
  clearSelection: () => set({ selectedItems: {} }),

  // UI
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  error: null,
  setError: (error) => set({ error }),

  // Results
  paymentSplits: null,
  setPaymentSplits: (splits) => set({ paymentSplits: splits }),
  clearPaymentSplits: () => set({ paymentSplits: null }),
}));
