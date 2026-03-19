// Telegram Mini App User
export interface TelegramUser {
  id: number;
  is_bot: boolean;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
}

// Room related types
export interface RoomParticipant {
  userId: string;
  username: string;
  firstName: string;
  selected: Record<string, number>; // item_id: quantity_selected
}

export interface ReceiptItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  assignedUsers: string[];
}

export interface Receipt {
  id: string;
  paidAt: string;
  tip: number;
  service: number;
  items: ReceiptItem[];
  totalSum: number;
}

export interface Room {
  id: string;
  creatorId: string;
  createdAt: string;
  isActive: boolean;
  receiptId: string | null;
  receipt?: Receipt;
  participants: RoomParticipant[];
  shareLink?: string;
  shareCode?: string;
}

export type RoomRole = 'creator' | 'participant';

// Payment calculation
export interface PaymentSplit {
  userId: string;
  username: string;
  items: Array<{
    name: string;
    quantity: number;
    price: number;
    subtotal: number;
  }>;
  subtotal: number;
  taxShare: number;
  tipShare: number;
  total: number;
}

// UI State
export type AppPage = 'home' | 'create-room' | 'room' | 'select-items' | 'results' | 'room-code';
